from django.core.management.base import BaseCommand

from server.apps.core.logic import actions


class Command(BaseCommand):
    def handle(self, *args, **options):
        actions.update_api_ignore()
        actions.update_api_proxy_configs()
