# -*- coding: utf-8 -*-

from django.db.models import Count, F

from server.apps.api.models import Domain
from server.apps.api.logic import notifier


MIN_IP_COUNT = 2


def alert_to_slack(domain_names):
    message = 'Blocked: {}'.format(', '.join(domain_names))
    notifier.slack_message(
        message=message,
        channel='#tests',
    )


def blocked_domains():
    return (Domain.objects
            .values('domain', 'client_hash')
            .distinct()
            .annotate(hash_count=Count('client_hash'))
            .values('domain', 'hash_count')
            .filter(hash_count__gte=MIN_IP_COUNT))


def check_blocked():
    domains = blocked_domains()
    if not domains:
        return
    alert_to_slack((domain['domain'] for domain in domains))
