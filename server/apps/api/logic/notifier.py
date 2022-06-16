import requests
from django.conf import settings


def slack_message(message):
    if settings.SLACK_WEBHOOK and message:
        response = requests.post(
            url=settings.SLACK_WEBHOOK,
            json={"text": message, "mrkdw": True},
        )

        if response.status_code == 200:
            return True

    return False
