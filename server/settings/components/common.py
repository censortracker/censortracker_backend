# -*- coding: utf-8 -*-

"""
Django settings for server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their config, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

from server.settings.components import BASE_DIR, config

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

SECRET_KEY = config("DJANGO_SECRET_KEY")

# Application definition:

INSTALLED_APPS = (
    # Default django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.gis.geoip2",
    # django-admin:
    "django.contrib.admin",
    # Authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # CORS:
    "corsheaders",
    # REST API:
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_api_key",
    # Pretty JSON Field
    "django_json_widget",
    # Your apps go here:
    "server.apps.api",
    "server.apps.core",
    "server.apps.users",
)

MIDDLEWARE = (
    # Django:
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
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
        "NAME": config("DB_NAME"),
        # You don't need these settings if using 'sqlite3':
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", default=5432, cast=int),
        "CONN_MAX_AGE": config("CONN_MAX_AGE", cast=int, default=60),
    },
}

EMAIL_PORT = 587
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "no-reply@censortracker.org"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en"

USE_I18N = True
USE_L10N = True

LANGUAGES = (
    ("en", "English"),
    ("ru", "Russian"),
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
            BASE_DIR.joinpath("server", "templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    }
]

STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = [
    BASE_DIR.joinpath("server", "static"),
]

MEDIA_URL = "/uploads/"
MEDIA_ROOT = os.path.join(BASE_DIR, "public", "uploads")

AUTH_USER_MODEL = "users.User"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

GEOIP_PATH = os.path.join(BASE_DIR, "server", "geoip")
GEOIP_COUNTRY = "GeoLite2-Country.mmdb"
GEOIP_CITY = "GeoLite2-City.mmdb"

# Allauth settings
LOGIN_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# Security
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework_api_key.permissions.HasAPIKey",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "server.apps.users.authentication.BearerTokenAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.AnonRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "150/day",
    },
}

# AWS S3 and GCS.
STORAGE_BUCKET_NAME = "censortracker"
STORAGE_OBJECT_FILENAME = "config.json"

# Third-party APIs
GITHUB_ACCESS_TOKEN = config("GITHUB_ACCESS_TOKEN")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
