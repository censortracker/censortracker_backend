import time

from django.core.management.base import BaseCommand
from djangorestframework_camel_case.util import camelize

from server.apps.api.logic.serializers import ConfigSerializer
from server.apps.core.logic import storages
from server.apps.core.models import Config


class Command(BaseCommand):
    def handle(self, *args, **options):
        config_queryset = Config.objects.all()
        config_serializer = ConfigSerializer(config_queryset, many=True)
        storages.upload(
            {
                "meta": {
                    "timestamp": int(time.time()),
                    "message": {
                        "title": None,
                        "description": None,
                        "show": False,
                        "type": "info|warning|error",
                        "page": "popup|options",
                    },
                    "geoIPServiceURL": "https://geo.censortracker.org/get-iso/",
                },
                "data": camelize(config_serializer.data),
            }
        )
