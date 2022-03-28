# -*- coding: utf-8 -*-

import os
import json

from django.core.management.base import BaseCommand

from server.apps.core.models import ProxyConfig
from server.apps.api.logic.serializers import ProxyConfigSerializer
from server.settings.components.common import BASE_DIR

PROXY_CONFIGS_PATH = BASE_DIR.joinpath("public", "api", "proxy-configs", "json")


class Command(BaseCommand):
    def handle(self, *args, **options):
        queryset = ProxyConfig.objects.active()
        serializer = ProxyConfigSerializer(queryset, many=True)

        if not os.path.exists(PROXY_CONFIGS_PATH):
            os.makedirs(PROXY_CONFIGS_PATH)

        with open(PROXY_CONFIGS_PATH / "index.json", "w") as fp:
            json.dump(serializer.data, fp)
