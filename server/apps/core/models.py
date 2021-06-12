# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(
        verbose_name=_("Name"), unique=True, max_length=512, null=False, blank=False
    )
    code = models.CharField(
        verbose_name=_("Country code"),
        unique=True,
        max_length=3,
        null=False,
        blank=False,
    )
    iso_a2_code = models.CharField(verbose_name=_('Alpha 2'), unique=True, max_length=2, null=True, blank=False)
    iso_a3_code = models.CharField(verbose_name=_('Alpha 3'), unique=True, max_length=3, null=True, blank=False)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Config(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, blank=False, null=False
    )
    registry_url = models.URLField(verbose_name=_("Registry URL"), null=False, blank=False)
    custom_registry_url = models.URLField(
        verbose_name=_("Custom Registry URL"), null=False, blank=False
    )
    report_endpoint = models.URLField(
        verbose_name=_("DPI API Endpoint"), null=False, blank=False
    )
    specifics = JSONField(
        verbose_name=_("Specifics"), blank=True, null=False, default=dict
    )

    class Meta:
        verbose_name = _("Config")
        verbose_name_plural = _("Configs")

    def __str__(self):
        return self.country.name
