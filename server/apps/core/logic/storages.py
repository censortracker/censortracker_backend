import json
import typing as t

import boto3
from django.conf import settings
from google.cloud.storage import Client


def update_config_gcs(data: t.Dict[str, t.Any]) -> None:
    """
    Uploads config to Google Cloud Storage.
    """
    client = Client.from_service_account_json(
        json_credentials_path=settings.GOOGLE_CREDENTIALS_PATH,
    )
    bucket = client.get_bucket(settings.STORAGE_BUCKET_NAME)
    blob = bucket.blob(settings.STORAGE_OBJECT_FILENAME)
    blob.cache_control = "no-cache, no-store, must-revalidate"

    with blob.open("w", content_type="application/json") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_config_aws(data: t.Dict[str, t.Any]) -> None:
    """
    Uploads config file to Amazon S3 bucket.
    """
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3.Object(settings.STORAGE_BUCKET_NAME, settings.STORAGE_OBJECT_FILENAME).put(
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


def upload(data) -> None:
    """
    Uploads config to all storages.

    Currently supported storages:
    - Google Cloud Storage
    - Amazon S3 (with CloudFront)
    """
    # update_config_gcs(data)
    update_config_aws(data)
