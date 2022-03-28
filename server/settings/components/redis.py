# -*- coding: utf-8 -*-

from server.settings.components.common import env

REDIS_HOST = env("REDIS_HOST")

RQ_QUEUES = {
    "default": {
        "HOST": REDIS_HOST,
        "PORT": 6379,
        "DB": 0,
        "DEFAULT_TIMEOUT": 350,
    },
}
