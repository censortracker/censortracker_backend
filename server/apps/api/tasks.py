# -*- coding: utf-8 -*-

"""
Celery Task for news grabber.
"""

from celery.schedules import crontab
from celery.task import PeriodicTask
from django.core.management import call_command


class IPData(PeriodicTask):
    name = "Update IP data"
    run_every = crontab(hour=1)
    # run_every = crontab()

    def run(self, *args, **kwargs):
        call_command("generate_case_hash")
        return True
