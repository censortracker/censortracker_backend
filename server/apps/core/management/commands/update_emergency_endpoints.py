import json

from django.core.management.base import BaseCommand
from django.utils import timezone
from github import Github

from server.settings.components.common import GITHUB_ACCESS_TOKEN


class Command(BaseCommand):
    @staticmethod
    def update_github_emergency_endpoints(config):
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

    def handle(self, *args, **options):
        configs = {
            "ignore": "https://app.censortracker.org/api/ignore/",
            "registry": "https://app.censortracker.org/api/config/",
            "proxy": "https://app.censortracker.org/api/proxy-config/",
        }
        self.update_github_emergency_endpoints(configs)
