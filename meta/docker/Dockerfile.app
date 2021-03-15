FROM alpine:latest

ENTRYPOINT ["/sbin/tini"]
WORKDIR /app

# Order is very relevant!!! // Sorted by chance of changes (less frequent first)
# Each step is cached on the buildhost, so right commands order prevents it from unneded rebuilds
# Change in any step will invalidate cache of all the next ones

ENV POETRY_VERSION=1.0.5 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN sed -e '/community/{p;s@v[^/]*/@edge/@;s@community@testing@}' -i /etc/apk/repositories && \
	apk update && \
	apk upgrade && \
	apk add \
		curl \
		sed \
		ca-certificates \
		zsh \
		python3 \
		tini \
		python3-dev \
		postgresql-dev \
		libffi-dev \
		musl-dev \
		gcc \
		dcron \
		postgresql-client \
		unit-python3 \
		unit \
	&& \
	chown 65534:65534 /app && \
	curl https://bootstrap.pypa.io/get-pip.py -LSso get-pip.py && \
	python3 get-pip.py && \
	pip install "poetry==$POETRY_VERSION" && poetry --version

COPY /meta/configs/unit.conf.json /var/lib/unit/conf.json
COPY --chown=65534:65534 /poetry.lock /pyproject.toml /app/

RUN poetry install --no-interaction --no-ansi

COPY /meta/sh /bin/

COPY --chown=65534:65534 /manage.py /app/
COPY --chown=65534:65534 /public /app/public/
COPY --chown=65534:65534 /server /app/server/
