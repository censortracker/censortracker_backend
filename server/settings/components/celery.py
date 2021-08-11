# -*- coding: utf-8 -*-

"""
Celery module
"""

from server.settings.components.common import env

REDIS_HOST = env("REDIS_HOST")

CELERYD_TASK_TIME_LIMIT = 60 * 60
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379/0"
