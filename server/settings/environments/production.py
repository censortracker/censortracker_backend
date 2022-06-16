# -*- coding: utf-8 -*-

"""
This file contains all the settings that defines the development server.

SECURITY WARNING: don't run with debug turned on in production!
"""
from server.settings.components.common import BASE_DIR

DEBUG = False

ALLOWED_HOSTS = ["*"]

# Static files:
# https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-STATICFILES_DIRS

# Adding STATIC_ROOT to collect static files via 'collectstatic'
STATIC_ROOT = BASE_DIR.joinpath("public", "static")

MEDIA_ROOT = BASE_DIR.joinpath("public", "uploads")
