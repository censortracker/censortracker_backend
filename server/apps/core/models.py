# -*- coding: utf-8 -*-

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.api.logic.managers import ProxyConfigManager


class Country(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        unique=True,
        max_length=512,
        null=False,
        blank=False,
    )
    code = models.CharField(
        verbose_name=_("Country code"),
        unique=True,
        max_length=3,
        null=False,
        blank=False,
    )
    iso_a2_code = models.CharField(
        verbose_name=_("Alpha 2"),
        max_length=2,
        null=True,
    )
    iso_a3_code = models.CharField(verbose_name=_("Alpha 3"), max_length=3, null=True)
    locale_code = models.CharField(
        verbose_name=_("Locale code"), max_length=8, null=True, default=None
    )
    active = models.BooleanField(verbose_name=_("Active"), default=False)

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
    name = models.CharField(
        verbose_name=_("Config name"),
        max_length=64,
        blank=False,
        null=False,
        unique=True,
    )
    server = models.CharField(
        verbose_name=_("Proxy server"),
        max_length=256,
        blank=False,
        null=False,
        unique=True,
    )
    port = models.CharField(
        verbose_name=_("Proxy port"), max_length=6, blank=False, null=False
    )
    ping_host = models.CharField(
        verbose_name=_("Proxy ping host"),
        max_length=256,
        blank=True,
        null=True,
    )
    ping_port = models.CharField(
        verbose_name=_("Proxy ping port"),
        max_length=6,
        blank=False,
        null=False,
        default=0,
    )
    weight = models.IntegerField(
        verbose_name=_("Weight"),
        null=False,
        blank=False,
        default=0,
    )

    active = models.BooleanField(
        verbose_name=_("Active"),
        default=False,
        null=False,
        blank=False,
    )

    objects = ProxyConfigManager()

    class Meta:
        ordering = ["-weight"]
        verbose_name = _("Proxy config")
        verbose_name_plural = _("Proxy Configs")

    def __str__(self):
        return f"{self.name}: <{self.server}:{self.port}>"

    def __repr__(self):
        return f"Proxy <{self.server}:{self.port}>"


class CountryRegistry(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, blank=False, null=False
    )
    domains = ArrayField(
        base_field=models.CharField(max_length=2048),
        blank=True,
    )

    class Meta:
        verbose_name = _("Country Registry")
        verbose_name_plural = _("Country Registries")

    def __str__(self):
        return self.country.name

    def __repr__(self):
        return f"CountryRegistry <{self.country.iso_a2_code}>"


class Ignore(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        unique=True,
        max_length=512,
        null=False,
        blank=False,
    )
    domains = ArrayField(
        base_field=models.TextField(),
        blank=True,
    )

    class Meta:
        verbose_name = _("Ignore")
        verbose_name_plural = _("Ignore")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Ignore <{self.name}>"
