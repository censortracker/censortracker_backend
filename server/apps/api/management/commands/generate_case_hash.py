# -*- coding: utf-8 -*-
import itertools
import json
import time
from typing import List

import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from django.core.management.base import BaseCommand
from django.db.models import Count, Max
from django.utils import timezone

from server.apps.api.logic import notifier
from server.apps.api.models import Case

MIN_CASE_COUNT_PER_DOMAIN = 2
SIGNIFICANT_CASES_PERIOD_DAYS = 3

REGISTRY_API_URL = "https://reestr.rublacklist.net/api/v2/domains/json/"

IGNORE = ["google.com"]

START_DATE = timezone.now() - timezone.timedelta(days=SIGNIFICANT_CASES_PERIOD_DAYS)
ONE_DAY_AGO = timezone.now() - timezone.timedelta(days=1)


def get_registry_domains() -> List[str]:
    try:
        response = requests.get(REGISTRY_API_URL, timeout=5)
        data = response.json()

        domains = set()

        for domain in data:
            if domain.startswith("*."):
                domains.add(domain[2:])

        return data
    except (ConnectionError, ConnectTimeout):
        return []


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_case_hash()
        alert_to_slack(get_cases())


def alert_to_slack(cases):
    if not cases:
        print("Nothing to report.")
        return

    blocked_domains = get_registry_domains()
    timestamp = timezone.now().strftime("%d-%m-%Y %H:%M:%S")

    final_cases = []

    for case in cases:
        domain = case.get("domain_name")

        if domain in blocked_domains or domain in IGNORE:
            continue

        final_cases.append(case)

    if not final_cases:
        return

    notifier.slack_message(f"📃 Отчет о DPI блокировках: *{timestamp}*")

    for case in final_cases:
        case_id = case.pop("case_id")
        domain_name = case.pop("domain_name")

        if domain_name in blocked_domains or domain_name in IGNORE:
            continue

        client_hash = case.pop("client_hash", "")[:8]
        values = "\n".join([str(x) for x in case.values() if x])
        notified = notifier.slack_message(
            f"[{domain_name}]\n{values}\n\n" f"Сигнатура: {client_hash}"
        )

        if notified:
            Case.objects.filter(pk=case_id).update(reported=True)

    notifier.slack_message(f"✅ Отчет сформирован, <@U0GBE515J>, <@U100MCJG7>")


def get_cases():
    unreported_cases = Case.objects.unreported().filter(created__gte=START_DATE)

    domains = (
        unreported_cases.values("domain__pk", "client_hash", "client_country__name")
        .distinct()
        .annotate(hash_count=Count("client_hash"))
        .values("domain__pk", "hash_count")
        .filter(hash_count__gte=MIN_CASE_COUNT_PER_DOMAIN)
        .annotate(latest_case=Max("created"))
        .filter(latest_case__gte=ONE_DAY_AGO)
        .values("domain__pk", "client_country__name")
    )

    ungrouped_cases = []

    for case in domains:
        last_cases_for_domains = (
            unreported_cases.filter(
                domain_id=case["domain__pk"],
                client_country__name=case["client_country__name"],
            )
            .values(
                "id",
                "domain__domain",
                "client_region",
                "client_provider",
                "client_country__name",
                "client_hash",
            )
            .distinct("domain__domain", "client_hash")
            .order_by("domain__domain")
        )

        ungrouped_cases.extend(list(last_cases_for_domains))

    cases_by_domains = []
    for domain_name, cases_by_domain in itertools.groupby(
        ungrouped_cases, key=lambda item: item["domain__domain"]
    ):
        for case_id, g in itertools.groupby(
            cases_by_domain, key=lambda item: item["id"]
        ):
            values = list(g)[0]
            cases_by_domains.append(
                {
                    "case_id": case_id,
                    "domain_name": domain_name,
                    "client_country": values["client_country__name"],
                    "client_region": values["client_region"],
                    "client_provider": values["client_provider"],
                    "client_hash": values["client_hash"],
                }
            )

    return cases_by_domains


def fetch_data_by_ip(ip):
    """Fetch data of client by IP.

    This endpoint is limited to 45 requests per minute from an IP address.

    If you go over the limit your requests will be throttled (HTTP 429) until
    your rate limit window is reset.

    If you constantly go over the limit your IP address will be banned for 1 hour.

    Your implementation should always check the value of the X-Rl header, and if its
    is 0 you must not send any more requests for the duration of X-Ttl in seconds.
    """
    response = requests.get(f"http://ip-api.com/json/{ip}")

    ttl = int(response.headers["X-Ttl"])
    rate_limit = int(response.headers["X-Rl"])

    if rate_limit == 0 or response.status_code == 429:
        time.sleep(ttl)

    return response.json()


def update_case_hash():
    allowed_country_codes = [
        "RU",
        "UA",
        "BY",
        "UZ",
        "KZ",
        "GE",
        "AZ",
        "LT",
        "MD",
        "LV",
        "KG",
        "TJ",
        "AM",
        "TM",
        "EE",
    ]

    cases = Case.objects.filter(
        client_hash="",
        client_ip__isnull=False,
        reported=False,
        client_country__iso_a2_code__in=allowed_country_codes,
    )
    for case in cases:
        try:
            ip_data = fetch_data_by_ip(case.client_ip)
        except json.decoder.JSONDecodeError:
            continue

        case.client_provider = ip_data["isp"]
        case.client_region = ip_data["regionName"]
        case.save()
        case.generate_hash()
