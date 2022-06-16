import json

from django.core.management.base import BaseCommand
from django.utils import timezone
from github import Github

from server.settings.components.common import GITHUB_ACCESS_TOKEN


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--domain', type=str, help='Domain for reserve hostname.')

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
            answer = input(f'Do you want to use {domain} as reserve hostname? (Y/n): ')
            hostname = f"https://app.{domain}"

            if 'y' in answer.lower():
                self.update_emergency_endpoints({
                    "ignore": f"{hostname}/api/ignore/",
                    "registry": f"{hostname}/api/config/",
                    "proxy": f"{hostname}/api/proxy-config/",
                })
