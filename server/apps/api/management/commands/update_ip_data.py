# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from server.apps.api.logic.ips_data import update_ip_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_ip_data()
