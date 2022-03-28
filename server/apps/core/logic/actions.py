import json
import os

from server.apps.api.logic.serializers import (
    IgnoreSerializer,
    ProxyConfigStatusSerializer,
)
from server.apps.core.models import Ignore, ProxyConfig
from server.settings.components.common import BASE_DIR

__all__ = ['update_api_ignore', 'update_api_proxy_configs']

API_PATH = BASE_DIR.joinpath("public", "api")


def _create_api_endpoint(*, scope, queryset, serializer_class) -> None:
    file_path = API_PATH.joinpath(scope, "json")

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    serializer = serializer_class(queryset, many=True)
    with open(file_path.joinpath("index.json"), "w") as fp:
        json.dump(serializer.data, fp)


def update_api_proxy_configs() -> None:
    _create_api_endpoint(
        scope="proxy-configs",
        queryset=ProxyConfig.objects.all(),
        serializer_class=ProxyConfigStatusSerializer
    )


def update_api_ignore() -> None:
    _create_api_endpoint(
        scope="ignore",
        queryset=Ignore.objects.all(),
        serializer_class=IgnoreSerializer,
    )
