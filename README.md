[![Logo](https://raw.githubusercontent.com/roskomsvoboda/censortracker/master/.github/readme-logo.png)](https://github.com/roskomsvoboda/censortracker_backend)

This Django project provides extremely simple API for writing and reading domains reported by [Censor Tracker](https://git.io/JfoBg). 
This is a part of the mechanism which will help us to detect DPI locks initiated by the government services.

Pre Requirements
================

- Docker
- PyCharm (or any other IDE/Editor)
- RabbitMQ


Configuring Rabbit
==================

On configuring Celery do not forget to add vhost for your stack, like this:

```
docker exec -i -t RABBIT_CONTAINER_ID_HERE bash -c 'rabbitmqctl set_permissions -p STACK_NAME_HERE RABBIT_USER_HERE ".*" ".*" ".*"'
```

In our case, `STACK_NAME` is vhost and can be `dev.censortracker` or `censortracker`.

Running
=======

Just run this command:
g
    ~ bash meta/local-dev/deploy.sh -s
    
 
API
===
 
This web-site provides two endpoints:

```
POST /case/
GET /domains/
```

License
=======

Censor Tracker is licensed under the MIT License. See LICENSE for more
information.
