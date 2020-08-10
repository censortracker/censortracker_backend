# -*- coding: utf-8 -*-

"""
Django settings for server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their config, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

from server.settings.components import BASE_DIR, env, secret

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

SECRET_KEY = secret("django.key")

# Application definition:

INSTALLED_APPS = (
    # Default django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",

    # REST API:
    "rest_framework",

    # Your apps go here:
    "server.apps.api",

)

MIDDLEWARE = (
    # Django:
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "server.urls"

WSGI_APPLICATION = "server.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        # Choices are: postgresql, mysql, sqlite3, oracle
        "ENGINE": "django.db.backends.postgresql",
        # Database name or filepath if using 'sqlite3':
        "NAME": env("DB_NAME"),
        # You don't need these settings if using 'sqlite3':
        "USER": env("DB_USER"),
        "PASSWORD": secret("pg.%s.passwd" % env("DJANGO_ENV")),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT", default=5432, cast=int),
        "CONN_MAX_AGE": env("CONN_MAX_AGE", cast=int, default=60),
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en"

USE_I18N = False
USE_L10N = False

LANGUAGES = (
    ("en", "English"),
)

USE_TZ = True
TIME_ZONE = "UTC"

# Templates
# https://docs.djangoproject.com/en/1.11/ref/templates/api

TEMPLATES = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # Contains plain text templates, like `robots.txt`:
            BASE_DIR.joinpath("server", "templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                # default template context processors
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    }
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
    ),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'axes_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

SLACK_WEBHOOK = secret('slack.dsn', default='')
