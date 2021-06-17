from django.core.management.base import BaseCommand

from server.apps.core.models import Country, Config


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for country in Country.objects.all():
            try:
                Config.objects.get(country=country)
            except Config.DoesNotExist:
                Config.objects.create(
                    country=country,
                    report_endpoint='https://dpi.censortracker.org/api/case/',
                )
