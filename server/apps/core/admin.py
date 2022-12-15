from django.contrib import admin, messages
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from server.apps.core.models import (
    Config,
    Country,
    CountryRegistry,
    Ignore,
    ProxyConfig,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "country",
        "country_code",
        "registry_url",
        "custom_registry_url",
    )
    list_per_page = 400
    ordering = ("registry_url",)
    search_fields = ("country__name", "country__code")

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget(attrs={"rows": 6, "cols": 90})},
    }

    @admin.display(description="Country Code")
    def country_code(self, obj):
        return obj.country.iso_a2_code


@admin.register(ProxyConfig)
class ProxyConfigAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "server",
        "port",
        "ping_host",
        "ping_port",
        "weight",
        "active",
    )

    def save_model(self, request, obj, form, change):
        messages.success(request, "API data for /api/proxy-configs/ updated!")
        super(ProxyConfigAdmin, self).save_model(request, obj, form, change)

    @admin.action(description="Mark selected as active")
    def make_active(self, request, queryset):
        queryset.update(active=True)
        messages.success(request, "Done!")

    @admin.action(description="Mark selected as inactive")
    def make_inactive(self, request, queryset):
        queryset.update(active=False)
        messages.success(request, "Done!")

    actions = [make_active, make_inactive]


@admin.register(CountryRegistry)
class CountryRegistryAdmin(admin.ModelAdmin):
    pass


@admin.register(Ignore)
class IgnoreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "domains",
    )

    def save_model(self, request, obj, form, change):
        messages.success(request, "API data for /api/ignore/ updated!")
        super(IgnoreAdmin, self).save_model(request, obj, form, change)
