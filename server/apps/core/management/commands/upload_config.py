import time

from django.core.management.base import BaseCommand
from djangorestframework_camel_case.util import camelize

from server.apps.api.logic.serializers import NewConfigSerializer
from server.apps.core.logic import storages
from server.apps.core.models import Config

AWS_CLOUDFRONT_CONFIG_URL = "https://d204gfm9dw21wi.cloudfront.net/"
AWS_S3_CONFIG_URL = "https://censortracker.s3.eu-central-1.amazonaws.com/config.json"


class Command(BaseCommand):
    def handle(self, *args, **options):
        config_queryset = Config.objects.all()
        config_serializer = NewConfigSerializer(config_queryset, many=True)
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
                    "geoIPServiceURL": "https://geo.censortracker.org/",
                },
                "data": camelize(config_serializer.data),
            }
        )
