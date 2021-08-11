# -*- coding: utf-8 -*-

from django.contrib.postgres.fields import JSONField
from django.db import models
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
    iso_a2_code = models.CharField(verbose_name=_("Alpha 2"), max_length=2, null=True)
    iso_a3_code = models.CharField(verbose_name=_("Alpha 3"), max_length=3, null=True)
    locale_code = models.CharField(
        verbose_name=_("Locale code"), max_length=8, null=True, default=None
    )

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
    registry_url = models.URLField(
        verbose_name=_("Registry URL"), null=True, blank=True
    )
    custom_registry_url = models.URLField(
        verbose_name=_("Custom Registry URL"), null=True, blank=True
    )
    report_endpoint = models.URLField(
        verbose_name=_("DPI API Endpoint"), null=True, blank=True
    )
    specifics = JSONField(
        verbose_name=_("Specifics"), blank=True, null=False, default=dict
    )

    class Meta:
        verbose_name = _("Config")
        verbose_name_plural = _("Configs")

    def __str__(self):
        return self.country.name


class ProxyConfig(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, _("Low")
        MEDIUM = 2, _("Medium")
        HIGH = 3, _("High")
        DEFAULT = 0, _("Default")

    name = models.CharField(
        verbose_name=_("Config name"), max_length=64, blank=False, null=False
    )
    server = models.CharField(
        verbose_name=_("Proxy server"), max_length=256, blank=False, null=False
    )
    port = models.CharField(
        verbose_name=_("Proxy server"), max_length=6, blank=False, null=False
    )
    ping_port = models.CharField(
        verbose_name=_("Proxy ping port"),
        max_length=6,
        blank=False,
        null=False,
        default=0,
    )
    priority = models.IntegerField(
        verbose_name=_("Priority"),
        choices=Priority.choices,
        default=Priority.DEFAULT,
        null=False,
        blank=True,
    )

    class Meta:
        ordering = ["-priority"]
        verbose_name = _("Proxy config")
        verbose_name_plural = _("Proxy Configs")

    def __str__(self):
        return f"{self.name}: <{self.server}:{self.port}>"

    def __repr__(self):
        return f"Proxy <{self.server}:{self.port}>"
