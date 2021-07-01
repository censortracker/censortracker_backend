from django.core.cache import caches
from rest_framework.throttling import AnonRateThrottle


class CreateCaseRateThrottle(AnonRateThrottle):
    rate = "200/day"
    cache = caches["api"]
    scope = "create_case_anon"


class DomainListRateThrottle(AnonRateThrottle):
    rate = "30000/day"
    caches = caches["api"]
    scope = "domain_list_anon"


class ProxyConfigListRateThrottle(AnonRateThrottle):
    rate = "120/day"
    caches = caches["api"]
    scope = "proxy_config_list_anon"


class ConfigRetrieveRateThrottle(AnonRateThrottle):
    rate = "5000/day"
    caches = caches["api"]
    scope = "retrieve_config_anon"
