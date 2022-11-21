from django.core.cache import caches
from rest_framework.throttling import AnonRateThrottle


class CountryListRateThrottle(AnonRateThrottle):
    rate = "300000/day"
    caches = caches["api"]
    scope = "country_list_anon"


class ProxyConfigListRateThrottle(AnonRateThrottle):
    rate = "300000/day"
    caches = caches["api"]
    scope = "proxy_config_list_anon"


class ConfigRetrieveRateThrottle(AnonRateThrottle):
    rate = "300000/day"
    caches = caches["api"]
    scope = "retrieve_config_anon"
