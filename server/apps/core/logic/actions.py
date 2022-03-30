import json
import os

from server.apps.api.logic.serializers import ProxyConfigStatusSerializer
from server.apps.core.models import Ignore, ProxyConfig
from server.settings.components.common import BASE_DIR

__all__ = ['update_api_ignore', 'update_api_proxy_configs']

API_PATH = BASE_DIR.joinpath("public", "api")


def create_api_endpoint(*, scope, data) -> None:
    file_path = API_PATH.joinpath(scope)

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open(file_path.joinpath("index.json"), "w") as fp:
        json.dump(data, fp)


def update_api_proxy_configs() -> None:
    queryset = ProxyConfig.objects.all()
    serializer = ProxyConfigStatusSerializer(queryset, many=True)

    data = []
    for item in serializer.data:
        item['pingHost'] = item['ping_host']
        item['pingPort'] = item['ping_port']

        del item['ping_host']
        del item['ping_port']
        data.append(item)

    create_api_endpoint(
        scope="proxy-configs",
        data=data,
    )


def update_api_ignore() -> None:
    data = []
    queryset = Ignore.objects.all()

    for obj in queryset:
        data.extend(obj.domains)

    create_api_endpoint(scope="ignore", data=data)
