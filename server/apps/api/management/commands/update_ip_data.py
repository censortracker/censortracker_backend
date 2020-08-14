# -*- coding: utf-8 -*-

import json
import hashlib
from time import sleep

import requests

from django.core.management.base import BaseCommand
from django.db.models import Count, Max
from django.utils import timezone

from server.apps.api.models import Case, Domain
from server.apps.api.logic import notifier


MIN_CASE_COUNT_PER_DOMAIN = 2
SIGNIFICANT_CASES_PERIOD_DAYS = 3


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_ip_data()
        check_blocked()


def alert_to_slack(domain_names):
    message = 'Blocked: {}'.format(', '.join(domain_names))
    notifier.slack_message(
        message=message,
        channel='#tests',
    )


def blocked_domains():
    start_date = (timezone.now() -
                  timezone.timedelta(days=SIGNIFICANT_CASES_PERIOD_DAYS))
    hour_ago = (timezone.now() -
                timezone.timedelta(hours=1))
    domain_pks = (Case.objects
                  .filter(created__gte=start_date)
                  .values('domain_id', 'client_hash')
                  .distinct()
                  .values('domain_id')
                  .annotate(hash_count=Count('client_hash'))
                  .values('domain_id', 'hash_count')
                  .filter(hash_count__gte=MIN_CASE_COUNT_PER_DOMAIN)
                  .annotate(latest_case=Max('created'))
                  .filter(latest_case__gte=hour_ago)
                  .values_list('domain', flat=True))
    return (Domain.objects
            .filter(pk__in=domain_pks)
            .values_list('domain', flat=True))


def check_blocked():
    domains = blocked_domains()
    if not domains:
        return
    alert_to_slack(domains)


def chunks(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i: i + size]


def fetch_data_chunk(ips_chunk):
    url = 'http://ip-api.com/batch'
    send_data = [{"query": ip, "fields": "isp,regionName"}
                 for ip in ips_chunk]
    response = requests.post(url, data=json.dumps(send_data))
    if response.status_code != 200:
        return []
    return json.loads(response.content)


def get_ips_data(ips):
    ratelimit = 15
    max_query_length = 100
    for minute_chunk in chunks(ips, ratelimit * max_query_length):
        for query_chunk in chunks(minute_chunk, max_query_length):
            data_chunk = fetch_data_chunk(query_chunk)
            for ip_data in data_chunk:
                yield ip_data
        sleep(60)


def hash_case_data(case):
    data = (case.client_ip +
            case.client_provider +
            case.client_region)
    return hashlib.sha256(data.encode()).hexdigest()


def update_ip_data():
    cases = Case.objects.filter(client_ip__isnull=False)
    ips = [case.client_ip for case in cases]
    ips_data = get_ips_data(ips)
    for (case, ip_data) in zip(cases, ips_data):
        if not ip_data:
            continue
        case.client_provider = ip_data['isp']
        case.client_region = ip_data['regionName']
        case.client_hash = hash_case_data(case)
        case.client_ip = None
        case.save()
