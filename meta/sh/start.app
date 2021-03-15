#!/bin/zsh -f

function get_secret() {
	local sec_path="${DOCKER_SECRETS_PATH:-/run/secrets}"
	< "${sec_path}/${PROJECT}.${1:-undefined}.secret"
}

function wait_for_db() {
	local cmd;
	case "$1" {
		(host)
			cmd="ping -c 1 -W 1 ${DB_HOST}"
			;;
		(up)
			cmd="db_ok"
			;;
	}
	for w ({1..120}) {
		sleep 1;
		${(z)cmd} &>/dev/null && return 0
	}
	print "DB is still unavailable after 120+ secs. Giving up. Please, consider restarting this container if needed."
	return 1
}

function db_ok() {
	manage dbshell <<< "SELECT 1;"
}

{
	if {wait_for_db host} {
		if {wait_for_db up} {
			manage migrate --noinput >/dev/null
		} else {
			print "Migrations are skipped due to database inavailability (although host is up). Please check what's happening)" >&2
			print "Reason:"
			db_ok
		}
	} else {
		print "Migrations skipped due to DB conatiner inavailability" >&2
	}
			manage collectstatic --noinput >/dev/null
		  chown 65534:65534 -R /app/public/static
		  chown 65534:65534 -R /app/public/uploads
} 2>&1

unitd --no-daemon --control unix:/var/run/control.unit.sock --log /dev/stdout

# vim: ft=zsh sw=2 ts=2
