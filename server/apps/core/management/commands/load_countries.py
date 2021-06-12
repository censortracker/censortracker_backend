import requests
from django.core.management.base import BaseCommand

from server.apps.core.models import Country


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.json"
        response = requests.get(url)

        for item in response.json():
            try:
                Country.objects.create(
                    name=item["name"],
                    code=item["country-code"],
                    iso_a2_code=item["alpha-2"],
                    iso_a3_code=item["alpha-3"],
                )
            except:
                continue
