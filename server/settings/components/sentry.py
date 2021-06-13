# -*- coding: utf-8 -*-

"""
Sentry configuration module
"""

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from server.settings.components import env, secret

SENTRY_DSN = secret("sentry.%s.dsn" % env("DJANGO_ENV"))

sentry_sdk.init(
    dsn=SENTRY_DSN, integrations=[DjangoIntegration(),], send_default_pii=True,
)
