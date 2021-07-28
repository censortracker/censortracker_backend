# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone

from server.apps.api.logic import notifier
from server.apps.api.models import Case, Domain

MIN_CASE_COUNT_PER_DOMAIN = 2
SIGNIFICANT_CASES_PERIOD_DAYS = 3


class Command(BaseCommand):
    def handle(self, *args, **options):
        start_date = timezone.now() - timezone.timedelta(days=30)
        cases = Case.objects.exclude(client_country__iso_a2_code="RU").filter(
            created__gte=start_date
        )

        domain_pks = (
            cases.values("domain__pk")
                .annotate(domains_count=Count("domain__pk"))
                .filter(domains_count__gte=2)
                .values_list("domain__pk", flat=True)
        )
        domains = Domain.objects.filter(pk__in=domain_pks).values_list("domain", flat=True)
        if domains:
            message = "Blocked: {}".format(", ".join(domains))
            notifier.slack_message(message=message)
            print(message)
