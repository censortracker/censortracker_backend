# -*- coding: utf-8 -*-

"""
Caching settings module
"""

from server.settings.components import config

REDIS_URL = config("REDIS_URL")

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": REDIS_URL,
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
    "api": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": REDIS_URL,
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
