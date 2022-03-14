# -*- coding: utf-8 -*-
import hashlib

from django.db import models

from server.apps.api.logic.managers import CaseManager
from server.apps.core.models import Country


class Domain(models.Model):
    domain = models.CharField(
        verbose_name="Domain",
        max_length=128,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def __str__(self):
        return self.domain


class Case(models.Model):
    domain = models.ForeignKey(
        Domain, on_delete=models.CASCADE, null=False, blank=False, related_name="cases"
    )
    client_ip = models.GenericIPAddressField(
        verbose_name="Client IP",
        null=True,
        blank=True,
    )
    client_hash = models.CharField(
        verbose_name="Client Hash", max_length=64, blank=True, default=""
    )
    client_region = models.CharField(
        verbose_name="Client region", max_length=128, blank=True, default=""
    )
    client_provider = models.CharField(
        verbose_name="Client provider", max_length=256, blank=True, default=""
    )
    created = models.DateTimeField(auto_now_add=True)

    client_country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    user_agent = models.TextField(verbose_name="User agent", null=True, blank=True)
    reported = models.BooleanField(default=False, null=False)

    objects = CaseManager()

    class Meta:
        verbose_name = "Case"
        verbose_name_plural = "Cases"

    def __str__(self):
        return f"Case <{self.client_hash}>"

    def generate_hash(self):
        if self.client_ip and self.client_region and self.client_provider:
            case_uid = f"{self.client_ip}{self.client_provider}{self.client_region}"
            self.client_hash = hashlib.sha256(case_uid.encode()).hexdigest()

            if self.client_ip:
                self.client_ip = None
            self.save()
