# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from server.apps.core.models import ProxyConfig


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--server", type=str, help="Host to update")
        parser.add_argument("--new-port", type=int, help="New port")

    def handle(self, *args, **options):
        server = options.get("server")
        new_port = options.get("new_port")

        if server and new_port:

            try:
                pc = ProxyConfig.objects.get(server__exact=server)
                print(f"Ping port update for {server}: {pc.port} -> {new_port}")
                pc.port = new_port
                pc.save()
            except ProxyConfig.MultipleObjectsReturned:
                print(f"Cannot update port for {server}")
