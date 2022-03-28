# -*- coding: utf-8 -*-

from server.settings.components.common import env

REDIS_HOST = env("REDIS_HOST")
REDIS_BROKER_URL = f"redis://{REDIS_HOST}:6379/0"
