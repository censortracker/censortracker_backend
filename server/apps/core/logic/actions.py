import os
import json

from server.apps.core.models import ProxyConfig, Ignore
from server.apps.api.logic.serializers import (
    ProxyConfigStatusSerializer,
    IgnoreSerializer,
)
from server.settings.components.common import BASE_DIR

PROXY_CONFIGS_PATH = BASE_DIR.joinpath("public", "api", "proxy-configs", "json")
IGNORE_PATH = BASE_DIR.joinpath("public", "api", "ignore", "json")


def update_api_proxy_configs():
    queryset = ProxyConfig.objects.all()
    serializer = ProxyConfigStatusSerializer(queryset, many=True)

    if not os.path.exists(PROXY_CONFIGS_PATH):
        os.makedirs(PROXY_CONFIGS_PATH)

    with open(PROXY_CONFIGS_PATH / "index.json", "w") as fp:
        json.dump(serializer.data, fp)


def update_api_ignore():
    queryset = Ignore.objects.all()
    serializer = IgnoreSerializer(queryset, many=True)

    if not os.path.exists(IGNORE_PATH):
        os.makedirs(IGNORE_PATH)

    with open(IGNORE_PATH / "index.json", "w") as fp:
        json.dump(serializer.data, fp)
