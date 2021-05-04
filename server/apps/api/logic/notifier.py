"""
Notification module
"""

import requests
from django.conf import settings


def slack_message(message, channel=None, app_name=None):
    """
    Send message to slack
    """
    if settings.DEBUG:
        return False

    if not message:
        return False

    if not channel:
        channel = "#registry-logs"

    if not app_name:
        app_name = "Registry Logger"

    if settings.SLACK_WEBHOOK:
        response = requests.post(
            url=settings.SLACK_WEBHOOK,
            json={
                "channel": channel,
                "text": message,
                "mrkdw": True,
                "username": app_name,
            },
        )

        if response.status_code == 200:
            return True

    return False
