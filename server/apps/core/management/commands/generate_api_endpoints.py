import json
import tempfile

import boto3
from django.core.management.base import BaseCommand
from google.cloud.storage import Client

from server.apps.api.logic.serializers import ConfigSerializer
from server.apps.core.models import Config
from server.settings.components.common import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    BASE_DIR,
    GOOGLE_CREDENTIALS_PATH,
    STORAGE_BUCKET_NAME,
    STORAGE_OBJECT_FILENAME,
)

AWS_CLOUDFRONT_CONFIG_URL = 'https://d204gfm9dw21wi.cloudfront.net/'
AWS_S3_CONFIG_URL = 'https://censortracker.s3.eu-central-1.amazonaws.com/config.json'


def upload_to_gcs(data):
    """
    Uploads config to Google Cloud Storage.
    """
    client = Client.from_service_account_json(
        json_credentials_path=GOOGLE_CREDENTIALS_PATH,
    )
    bucket = client.get_bucket(STORAGE_BUCKET_NAME)
    blob = bucket.blob(STORAGE_OBJECT_FILENAME)
    blob.cache_control = "no-cache, no-store, must-revalidate"

    with blob.open("w", content_type="application/json") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return blob.public_url


def upload_to_aws(data):
    """
    Uploads config file to Amazon S3 bucket.
    """
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    s3.Object(STORAGE_BUCKET_NAME, STORAGE_OBJECT_FILENAME).put(
        Body=bytes(
            json.dumps(
                obj=data,
                indent=2,
                ensure_ascii=False,
            ).encode("utf-8"),
        ),
        ContentType="application/json",
        CacheControl="no-cache, no-store",
    )


class Command(BaseCommand):

    def upload_to_storages(self, data):
        upload_to_gcs(data)
        upload_to_aws(data)

    def handle(self, *args, **options):
        config_queryset = Config.objects.all()
        config_serializer = ConfigSerializer(config_queryset, many=True)
        self.upload_to_storages(config_serializer.data)
