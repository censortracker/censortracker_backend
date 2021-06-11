# -*- coding: utf-8 -*-

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

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name


class Config(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, blank=False, null=False
    )
