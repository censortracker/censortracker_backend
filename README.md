[![Logo](https://raw.githubusercontent.com/roskomsvoboda/censortracker/master/.github/censortracker-popups.svg)](https://github.com/roskomsvoboda/censortracker_backend)

This Django project provides extremely simple API for writing and reading domains reported by [Censor Tracker](https://git.io/JfoBg). 
This is a part of the mechanism which will help us to detect DPI locks initiated by the government services.

Pre Requirements
================

- Docker
- PyCharm (or any other IDE/Editor)

Running
=======

Just run this command:

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
