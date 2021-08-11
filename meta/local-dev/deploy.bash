#!/usr/bin/env bash
# vim: ft=sh ts=2 sw=2
# functions (definition block) {{{
# printers() { (little functions to format output) {{{
clrzr() {
	local echo_opt="-e" ask=""
	while getopts ":c:na" o; do
		case "${o}" in
			n)
				echo_opt="-ne"
				;;
			a)
				echo_opt="-ne"
				ask=": "
				;;
			c)
				color="${OPTARG}"
				;;
			*)
				;;
		esac
	done
	shift $((OPTIND-1))
	unset o OPTIND OPTARG OPTERR
	echo "${echo_opt}" "${COLOR:+\e[1;${color}m*\e[0m} ${*}${COLOR:+\e[0m${ask+\a}}${ask}";
}
err() { clrzr -c 31 "${@}"; }
die() { err "${@}"; exit 1; }
inf() { clrzr -c 32 "${@}"; }
wrn() { clrzr -c 33 "${@}"; }
ask() { clrzr -c 35 -a "${@}"; }
# /printers }}}
# function cmd() { (does command exist?) {{{
function cmd() { command -v "${@}" &>/dev/null; }
# /cmd }}}
function checks() { # (Various checks) {{{
	if cmd "${PYTHON:-python3}"; then
		export PYTHON="${PYTHON:-python3}"
	elif cmd python; then
		export PYTHON=python
	else
		die "Neither 'python3' nor 'python' was found (we need it to run settings checker)! HINT: you can set PYTHON variable with path to it"
	fi
	cmd "${SED}" || die "Can't find '${SED}' program (we need it for placeholders replacement)! HINT: you can set SED variable with path to it"
	cmd "${DOCKER:-docker}" || die "Can't find 'docker' program (well, this script is useless without it)! HINT: you can set DOCKER variable with path to it"
	cmd "${GIT:-git}" || die "Can't find 'git' program (how did you checked out this repo then? O_o)! HINT: you can set GIT variable with path to it"
	unalias grep &>/dev/null
	unset -f grep &>/dev/null
	if [[ "${BASH_VERSION::1}" -lt 5 ]]; then
		die "Please, upgrade your 'bash'. We need a modern version to work correctly."
	fi
}
# /checks }}}
function docker_exists() { # (Does entity ($1) with name ($2) exists on docker stack? ) {{{
	local what="${1}"
	local name="${2}"
	local grpchk=${3+--}
	local grpflg="${grpchk:--q}"
	if [[ "${what}" == "stack" ]]; then # `stack ls` is not consistent with others about `-q` and `-f`
		docker "${what}" ls | grep "${grpflg}" "${name}"
	else
		docker "${what}" ls -q -f "name=${name}" | grep "${grpflg}" "."
	fi
}
# /docker_exists }}}
function add_secret() { # (Adds Docker Secret (if it doesn't exist yet)) {{{
	local secret_name="${1}"
	if ! docker_exists secret "${secret_name}"; then
		ask "Please, provide a value for the secret named '${secret_name}' (see the settings module code for details)"
		read -r secret_value
		( echo -n "${secret_value}" | docker secret create "${secret_name}" - ) || die "Failed to add secret (while all of them is mandatory)"
	fi
}
# /add_secret }}}
function get_entities() { # (gets secrets/networks/volumes/whatever from compose) {{{
	local content=() entity="${1}" compose="${2:-tmp/docker-compose.yml}"
	readarray -t content < <(
		${SED} -n "/^${entity}:/,/^[^ ]/{/^  [^:]*:\$/{s@:\$@@;p}}" "${compose}"
	)
	echo "${content[@]}"
}
# /get_entities }}}
# /functions }}}

# Variables {{{
export GREP_OPTIONS="" GREP_COLOR="" GREP_COLORS=""
while getopts ":w:d:askKfCc" o; do
	case "${o}" in
		a)
			ONLY_APP=1
			;;
		w)
			WAIT_FOR_CONTAINERS="${OPTARG}"
			;;
		d)
			DUMP_FILE="${OPTARG}"
			;;
		k)
			RESTART_STACK=1
			;;
		K)
			RESTART_STACK=0
			;;
		f)
			I_WANT_TO_TRY_ON_MY_OS=1
			;;
		s)
			SKIP_DUMP=1
			;;
		c)
			CLEAN_DB=1
			;;
		C)
			NOCOLOR=1
			;;
		*)
			;;
	esac
done
shift $((OPTIND-1))
unset o OPTIND OPTARG OPTERR
export PROJECT="${PROJECT:-censortracker}"
export CI_PROJECT_NAME="${PROJECT}"
export CI_REGISTRY_IMAGE="${IMAGES_PREFIX:-${CI_PROJECT_NAME}-imgs}"
export DUMP_FILE="${DUMP_FILE:-tmp/${PROJECT}.pgdump}"
export DJANGO_ENV="${DJANGO_ENV:-development}"
case $(uname -s) in
	Linux)
		LO_IFNAME="lo"
		SED=${SED:-sed}
		;;
	Darwin)
		LO_IFNAME="lo0"
		SED=${SED:-sed}
		;;
	*)
		if [[ -z "${I_WANT_TO_TRY_ON_MY_OS}" ]]; then
			err "This script wasn't tested to work on your OS. Most ptobably it will fail. So, we're aborting the work."
			die "If you want to try the luck - set I_WANT_TO_TRY_ON_MY_OS variable to any value or use '-f' switch"
		fi
		;;
esac
if [[ -z "${NOCOLOR}" ]]; then
	COLOR=1
fi
# /Variables }}}

inf "Let's perform some checks and deploy our docker stack for local development!"

if [[ -f "tmp/.db_imported" ]]; then
	inf "Looks like DB was already imported. Skipping dump restoration..."
	SKIP_DUMP=1
fi

if ! [[ -d meta/local-dev ]]; then
	cd "$(git rev-parse --show-toplevel)" || die "Failed to find repository root!"
fi

checks && inf "All Pre-Use checks are passed. Good!"

if ! docker_exists node "" &>/dev/null; then
	wrn "We're using Swarm for deployment, but this node is not configured as Swarm node."
	inf "Creating Swarm cluster..."
	docker swarm init --advertise-addr "${LO_IFNAME}" || die "Swarm initialization failed! Look above log for errors (maybe you'll want to set LO_IFNAME to the name of your localhost interface (if it is not '${LO_IFNAME}')."
fi

inf "Checking if we have mandatory docker networks"
docker_exists network bridge || die "default docker bridge network doesn't exist! Something strange!"
if ! docker_exists network int; then
	docker network create --attachable -d overlay --scope swarm --subnet 100.66.0.0/16 int >/dev/null || die "Failed to create network 'int' (but we need it for proper work of the stack)"
fi

if docker_exists stack "${CI_PROJECT_NAME}"; then
	if [[ -z "${RESTART_STACK}" ]]; then
		wrn "Already running stack with same name ('${PROJECT}') is deteced!"
		wrn "If that's not an our copy - try to set PROJECT variable to something different than ${PROJECT}"
		err "You can do either of that:"
		err "- Set RESTART_STACK variable to '1', or use '-k' option to automatically restart it, or"
		err "- Set RESTART_STACK variable to '0', or use '-K' option to disale restart (and deploy/update services there)"
		die "Unfortunately, you did not select any of proposed options, so we're failing"
	elif [[ "${RESTART_STACK}" -eq 1 ]]; then
		docker stack rm "${PROJECT}" || die "Failed to remove stack ${PROJECT}"
	fi
fi

inf "Preparing Docker-related files for deployment (mostly, placeholders replacement)..."

${SED} \
	-e "s#%IMAGE_APP%#${CI_REGISTRY_IMAGE}/app#g" \
	-e "s#%IMAGE_WEB%#${CI_REGISTRY_IMAGE}/web#g" \
	-e "s#%PROJECT%#${CI_PROJECT_NAME}#g" \
	-e "s#%DJANGO_ENV%#${DJANGO_ENV}#g" \
	meta/local-dev/docker-compose.yml > tmp/docker-compose.yml || die "Failed"

inf "Building Docker images..."

build_images=()
build_images+=("app::meta/docker/Dockerfile.app")

if [[ -z "${ONLY_APP}" ]]; then
	build_images+=("web::meta/local-dev/Dockerfile.web")
fi
for img in "${build_images[@]}"; do
	img_name="${img%%::*}" dock_file="${img##*::}"
	docker build --network host -t "${CI_REGISTRY_IMAGE}/${img_name}" -f "${dock_file}" . || die "Failed to build container '${img_name}' using '${dock_file}'"
done
unset img img_name dock_file

inf "Checking if stack is ready to deploy (all secrets are set)"

for secname in $(get_entities secrets); do
	add_secret "${secname}" || die "Failed to add secret '${secname}'"
done
unset secname

inf "Adding docker volumes..."
for v in $(get_entities volumes); do
	volname="${PROJECT}_${v}"
	if ! docker_exists volume "${volname}"; then
		docker volume create "${volname}" || die "Failed to create volume '${volname}'"
	elif [[ -n "${CLEAN_DB}" && "${v}" == "pgbase" ]]; then
		inf "DB cleanup was requested"
		docker volume rm -f "${volname}" || die "Failed to drop DB volume"
		docker volume create "${volname}" || die "Failed to create volume '${volname}'"
	fi
done
unset v volname

inf "Deploying stack..."
docker stack deploy -c tmp/docker-compose.yml "${PROJECT}" || die "Deployment failed"
inf "Stack deployed!"
if [[ -z "${SKIP_DUMP}" ]]; then
	WAIT_FOR_CONTAINERS=${WAIT_FOR_CONTAINERS:-30}
	inf "Waiting ${WAIT_FOR_CONTAINERS} seconds (that DB container would start)..."
	inf "Hint: use WAIT_FOR_CONTAINERS variable or '-w' option to change the timeout"
	inf "Hint2: You can set SKIP_DUMP variable or use '-s' option to skip restoration of the dump (if you don't need it)"
	sleep "${WAIT_FOR_CONTAINERS}"

	inf "Checking if DB container is running (it should be already)..."
	db_id=$(docker_exists container "${PROJECT}_${PROJECT}-db" "get_name")
	# TODO: ^ unhardcode continer name
	if [[ -z "${db_id}" ]]; then
		err "Can't find DB container in the list of running containers"
		die "Consider setting WAIT_FOR_CONTAINERS to value larger than ${WAIT_FOR_CONTAINERS}"
	fi
	inf "Importing DB dump in the local instance..."
	if [[ -f "${DUMP_FILE}" ]]; then
		docker exec -i "${db_id}" pg_restore -O -Upostgres -d postgres < "${DUMP_FILE}" || die "Importing failed :'("
		# TODO: ^ maybe unhardcode "postgres" from here and from the containers.
		touch tmp/.db_imported
	else
		err "Can't find a DB dump at the ${DUMP_FILE}."
		err "This means that database would be empty, and, most probably, you will be unable to test anything."
		err "Although, everything already deployed and started, so you can give it a try (and, maybe, fill the DB yourself."
		err "If this is the case - just ignore that error."
		err "Otherwise, either:"
		err "  - put DB dump (not an sql-script) file (you can as admins for it, if you haven't yet fetched it) at '${DUMP_FILE}', or"
		err "  - provide another path to the dump file with either DUMP_FILE variable or '-d' option"
		die "Done (see above)!"
	fi
else
	inf "Skipping dump restoration as requested"
fi
inf "Done!"
