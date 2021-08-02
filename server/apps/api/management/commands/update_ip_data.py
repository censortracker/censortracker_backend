# -*- coding: utf-8 -*-
import hashlib
import itertools
import json
from time import sleep

import requests
from django.core.management.base import BaseCommand
from django.db.models import Count, Max
from django.utils import timezone

from server.apps.api.logic import notifier
from server.apps.api.models import Case

MIN_CASE_COUNT_PER_DOMAIN = 2
SIGNIFICANT_CASES_PERIOD_DAYS = 3


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_ip_data()
        check_blocked()


def alert_to_slack(cases_by_domains):
    messages = []
    for case in cases_by_domains:
        domain_name = case.pop("domain_name")
        values = "\n".join([x for x in case.values() if x])
        messages.append(f"[{domain_name}]\n{values}")
    message = "\n\n".join(messages)
    notifier.slack_message(message=message)


def blocked_domains():
    start_date = timezone.now() - timezone.timedelta(days=SIGNIFICANT_CASES_PERIOD_DAYS)
    hour_ago = timezone.now() - timezone.timedelta(hours=1)
    cases = Case.objects.filter(created__gte=start_date)

    domain_pks = (
        cases.values("domain__pk", "client_hash")
        .distinct()
        .annotate(hash_count=Count("client_hash"))
        .values("domain__pk", "hash_count")
        .filter(hash_count__gte=MIN_CASE_COUNT_PER_DOMAIN)
        .annotate(latest_case=Max("created"))
        .filter(latest_case__gte=hour_ago)
        .values_list("domain__pk", flat=True)
    )
    last_cases_for_domains = (
        cases.filter(created__gte=hour_ago, domain_id__in=domain_pks)
        .values(
            "id", "domain__domain", "client_region", "client_provider", "client_country"
        )
        .order_by("domain__domain")
    )

    cases_by_domains = []
    for domain_name, cases_by_domain in itertools.groupby(
        last_cases_for_domains, key=lambda item: item["domain__domain"]
    ):
        for case_id, g in itertools.groupby(
            cases_by_domain, key=lambda item: item["id"]
        ):
            values = list(g)[0]
            cases_by_domains.append(
                {
                    "domain_name": domain_name,
                    "client_country": values["client_country"],
                    "client_region": values["client_region"],
                    "client_provider": values["client_provider"],
                }
            )

    return cases_by_domains


def check_blocked():
    cases_by_domains = blocked_domains()
    if not cases_by_domains:
        print("No new domains found")
        return
    alert_to_slack(cases_by_domains)


def chunks(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def fetch_data_chunk(ips_chunk):
    url = "https://ip-api.com/batch"
    send_data = [{"query": ip, "fields": "isp,regionName"} for ip in ips_chunk]
    response = requests.post(url, data=json.dumps(send_data))
    if response.status_code != 200:
        return []
    return json.loads(response.content)


def get_ips_data(ips):
    rate_limit = 15
    max_query_length = 100
    for minute_chunk in chunks(ips, rate_limit * max_query_length):
        for query_chunk in chunks(minute_chunk, max_query_length):
            data_chunk = fetch_data_chunk(query_chunk)
            for ip_data in data_chunk:
                yield ip_data
        sleep(60)


def generate_case_hash(case):
    data = case.client_ip + case.client_provider + case.client_region
    return hashlib.sha256(data.encode()).hexdigest()


def update_ip_data():
    cases = Case.objects.filter(
        client_ip__isnull=False, client_country__iso_a2_code="RU"
    )
    ips = [case.client_ip for case in cases]
    ips_data = get_ips_data(ips)
    for (case, ip_data) in zip(cases, ips_data):
        if not ip_data:
            continue
        case.client_provider = ip_data["isp"]
        case.client_region = ip_data["regionName"]
        case.client_hash = generate_case_hash(case)
        case.client_ip = None
        case.save()
