from django.contrib import admin, messages

from server.apps.core.models import (
    Config,
    Country,
    CountryRegistry,
    ProxyConfig,
)
from server.apps.core.logic import actions


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("country",)


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
        try:
            actions.update_api_proxy_configs()
            messages.success(request, 'API data for /api/proxy-configs/ updated!')
        except:
            messages.error(request, 'Error on updating /api/proxy-configs/')
        super(ProxyConfigAdmin, self).save_model(request, obj, form, change)

    def make_active(self, request, queryset):
        queryset.update(active=True)
        messages.success(request, "Done!")

    def make_inactive(self, request, queryset):
        queryset.update(active=False)
        messages.success(request, "Done!")

    make_active.short_description = "Mark selected as active"
    make_inactive.short_description = "Mark selected as inactive"

    actions = ["make_active", "make_inactive"]


@admin.register(CountryRegistry)
class CountryRegistryAdmin(admin.ModelAdmin):
    pass
