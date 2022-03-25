from django.core.cache import caches
from rest_framework.throttling import AnonRateThrottle


class CreateCaseRateThrottle(AnonRateThrottle):
    rate = "1000/day"
    cache = caches["api"]
    scope = "create_case_anon"


class DomainListRateThrottle(AnonRateThrottle):
    rate = "20000/day"
    caches = caches["api"]
    scope = "domain_list_anon"


class CountryListRateThrottle(AnonRateThrottle):
    rate = "5000/day"
    caches = caches["api"]
    scope = "country_list_anon"


class ProxyConfigListRateThrottle(AnonRateThrottle):
    rate = "10000/day"
    caches = caches["api"]
    scope = "proxy_config_list_anon"


class ConfigRetrieveRateThrottle(AnonRateThrottle):
    rate = "10000/day"
    caches = caches["api"]
    scope = "retrieve_config_anon"
