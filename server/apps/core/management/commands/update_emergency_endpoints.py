import json

from django.core.management.base import BaseCommand
from django.utils import timezone
from github import Github

from server.apps.core.models import Config
from server.settings.components.common import GITHUB_ACCESS_TOKEN


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--domain", type=str, help="Domain for reserve hostname.")

    @staticmethod
    def update_emergency_endpoints(config):
        assert GITHUB_ACCESS_TOKEN, "GITHUB_ACCESS_TOKEN cannot be None"

        github = Github(GITHUB_ACCESS_TOKEN)
        repo = github.get_repo("roskomsvoboda/ctconf")
        endpoints_file_path = "endpoints.json"
        endpoints_file = repo.get_contents(endpoints_file_path)
        content = json.dumps(config, sort_keys=True, ensure_ascii=False, indent=2)
        repo.update_file(
            path=endpoints_file_path,
            message=f"Updated config: {timezone.now(): %d-%m-%Y %MM:%HH}",
            content=content,
            sha=endpoints_file.sha,
        )

    def handle(self, domain, *args, **options):
        if domain is not None:
            answer = input(f"Do you want to use {domain} as reserve hostname? (Y/n): ")

            if "y" in answer.lower():
                self.update_emergency_endpoints(
                    {
                        "ignore": f"https://app.{domain}/api/ignore/",
                        "registry": f"https://app.{domain}/api/config/",
                        "proxy": f"https://app.{domain}api/proxy-config/",
                    }
                )

                up_yn = input('Do you want to update records in database? (Y/n): ')

                if 'y' in up_yn.lower():
                    specifics = {
                        'cooperationRefusedORIUrl':
                            f'https://registry.{domain}/api/v3/ori/refused/json/',
                    }
                    registry_url = f'https://registry.{domain}/api/v3/domains/json/'
                    custom_registry_url = f'https://registry.censortracker.org/api/v4/dpi/ru/json/'

                    for config in Config.objects.all():
                        config.registry_url = registry_url
                        config.specifics = specifics
                        config.custom_registry_url = custom_registry_url
                        config.save()
