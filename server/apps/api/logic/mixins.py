from django.contrib.gis.geoip2 import GeoIP2
from ipware import get_client_ip


class ClientIPMixin:
    def get_client_ip(self, request: bool = None):
        client_ip, is_routable = get_client_ip(request or self.request)

        if client_ip is None:
            return None
        else:
            if is_routable:
                return client_ip
        return None

    def get_client_country_code(self):
        geo = GeoIP2()
        ip = self.get_client_ip()

        if ip is not None:
            country = geo.country(ip)
            return country["country_code"]

        return None
