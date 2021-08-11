"""
Notification module
"""

import requests
from django.conf import settings


def slack_message(message):
    """
    Send message to slack
    """
    if settings.SLACK_WEBHOOK and message:
        response = requests.post(
            url=settings.SLACK_WEBHOOK, json={"text": message, "mrkdw": True},
        )

        if response.status_code == 200:
            return True

    return False
