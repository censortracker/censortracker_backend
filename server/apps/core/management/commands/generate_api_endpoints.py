import json
import tempfile

from django.core.management.base import BaseCommand
from google.cloud.storage import Client

from server.apps.api.logic.serializers import ConfigSerializer
from server.apps.core.models import Config

from server.settings.components.common import (
    BASE_DIR,
    GOOGLE_CLOUD_STORAGE_BUCKET,
    GOOGLE_CREDENTIALS_PATH,
)

CONFIG_FILENAME = 'config.json'


def upload_to_gcs(data):
    client = Client.from_service_account_json(
        json_credentials_path=GOOGLE_CREDENTIALS_PATH,
    )
    bucket = client.get_bucket(GOOGLE_CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(CONFIG_FILENAME)
    blob.cache_control = 'no-cache, no-store, must-revalidate'

    with blob.open('w', content_type="application/json") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return blob.public_url


class Command(BaseCommand):
    def handle(self, *args, **options):
        config_queryset = Config.objects.all()
        config_serializer = ConfigSerializer(config_queryset, many=True)
        upload_to_gcs(config_serializer.data)
