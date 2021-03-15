# -*- coding: utf-8 -*-

from django.contrib import admin

from server.apps.api.models import Domain, Case


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    pass


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    pass
