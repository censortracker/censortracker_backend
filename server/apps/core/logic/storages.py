import json
import typing as t

import boto3
from github import Github
from django.conf import settings
from django.utils import timezone


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


def update_config_github(data: t.Dict[str, t.Any]) -> None:
    github = Github(settings.GITHUB_ACCESS_TOKEN)
    repo = github.get_repo(settings.GITHUB_CONFIG_REPOSITORY)
    endpoints_file = repo.get_contents(settings.STORAGE_OBJECT_FILENAME)
    content = json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2)
    repo.update_file(
        path=settings.STORAGE_OBJECT_FILENAME,
        message=f"Updated config: {timezone.now(): %d-%m-%Y %MM:%HH}",
        content=content,
        sha=endpoints_file.sha,
    )


def upload(data) -> None:
    """
    Uploads config to all storages.

    Currently supported storages:
    - Google Cloud Storage
    - Amazon S3 (with CloudFront)
    """
    update_config_aws(data)
    update_config_github(data)
