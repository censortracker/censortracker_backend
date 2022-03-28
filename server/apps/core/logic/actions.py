import os
import json

from server.apps.core.models import ProxyConfig
from server.apps.api.logic.serializers import ProxyConfigSerializer
from server.settings.components.common import PROXY_CONFIGS_PATH


def update_api_proxy_configs():
    queryset = ProxyConfig.objects.active()
    serializer = ProxyConfigSerializer(queryset, many=True)

    if not os.path.exists(PROXY_CONFIGS_PATH):
        os.makedirs(PROXY_CONFIGS_PATH)

    with open(PROXY_CONFIGS_PATH / "index.json", "w") as fp:
        json.dump(serializer.data, fp)
