#!/usr/bin/env python3
"""
Local deployment helper to track missing secrets (and modules, that used in settings)
"""
import re

try:
    import server.settings  # pylint: disable=unused-import
except ModuleNotFoundError as err:
    try:
        MOD_NAME = re.search("No module named '(.+?)'", str(err)).group(1)
    except AttributeError:
        MOD_NAME = ""
    if MOD_NAME:
        print("MODULE::%s" % MOD_NAME)
        exit(1)
except Exception as err:  # pylint: disable=broad-except
    try:
        ENV_NAME = re.search('"(.+?)" is not defined', str(err)).group(1)
    except AttributeError:
        ENV_NAME = ""
    if ENV_NAME:
        print("ENV::%s" % ENV_NAME)
        exit(1)
    try:
        SECRET_NAME = re.search(
            r'Secret "(.+?)" \([^\)]*\) is missing', str(err)
        ).group(1)
        # ^ r'' because both pylint and flake8 cries about \) otherwise :-/
    except AttributeError:
        SECRET_NAME = ""
    if SECRET_NAME:
        print("SECRET::%s" % SECRET_NAME)
        exit(1)

exit(0)
