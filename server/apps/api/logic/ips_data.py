# -*- coding: utf-8 -*-

import json
import hashlib
from time import sleep

import requests

from server.apps.api.models import Domain


def chunks(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i: i + size]


def fetch_data_chunk(ips_chunk):
    url = 'http://ip-api.com/batch'
    send_data = [{"query": ip, "fields": "isp,regionName"}
                 for ip in ips_chunk]
    response = requests.post(url, data=json.dumps(send_data))
    if response.status_code != 200:
        return
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


def hash_domain_data(domain):
    data = (domain.client_ip +
            domain.domain +
            domain.client_provider +
            domain.client_region)
    return hashlib.sha256(data.encode()).hexdigest()


def new_domains():
    return Domain.objects.filter(client_ip__isnull=False)


def update_ip_data():
    domains = new_domains()
    ips = [domain.client_ip for domain in domains]
    ips_data = get_ips_data(ips)
    for (domain, ip_data) in zip(domains, ips_data):
        if not ip_data:
            continue
        domain.client_provider = ip_data['isp']
        domain.client_region = ip_data['regionName']
        domain.client_hash = hash_domain_data(domain)
        domain.client_ip = None
        domain.save()
