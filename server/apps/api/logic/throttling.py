from django.core.cache import caches
from rest_framework.throttling import AnonRateThrottle


class CreateCaseRateThrottle(AnonRateThrottle):
    cache = caches['api']
