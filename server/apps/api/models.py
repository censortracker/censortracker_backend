# -*- coding: utf-8 -*-

from django.db import models


class Domain(models.Model):
    domain = models.CharField(
        verbose_name='Domain',
        max_length=128,
        null=False,
        blank=False,
    )
    client_ip = models.GenericIPAddressField(
        verbose_name='Client IP',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'

    def __str__(self):
        return self.domain
