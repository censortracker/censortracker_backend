# -*- coding: utf-8 -*-

"""
Caching settings module
"""

from server.settings.components.common import env

REDIS_HOST = env("REDIS_HOST")

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": f"{REDIS_HOST}:6379",
        "OPTIONS": {
            "DB": 1,
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "CONNECTION_POOL_CLASS": "redis.BlockingConnectionPool",
            "CONNECTION_POOL_CLASS_KWARGS": {"max_connections": 50, "timeout": 20},
            "MAX_CONNECTIONS": 1000,
            "PICKLE_VERSION": -1,
        },
        "TIMEOUT": 345600,
    },
}
