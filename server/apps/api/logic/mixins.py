from django.contrib.gis.geoip2 import GeoIP2
from ipware import get_client_ip


class ClientIPMixin:
    def get_client_ip(self):
        client_ip, is_routable = get_client_ip(self.request)

        if client_ip and is_routable:
            return client_ip

        return None

    def get_client_country_code(self):
        geo = GeoIP2()
        client_ip = self.get_client_ip()

        custom_country_code = self.request.query_params.get("countryCode")

        if custom_country_code is not None:
            return custom_country_code

        if client_ip is not None:
            country = geo.country(client_ip)
            return country["country_code"]

        return None
