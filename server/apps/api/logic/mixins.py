from ipware import get_client_ip


class ClientIPMixin:

    def get_client_ip(self, request):
        client_ip, is_routable = get_client_ip(request)
        if client_ip is None:
            return None
        else:
            if is_routable:
                return client_ip

        # Return None when is not routable
        return client_ip
