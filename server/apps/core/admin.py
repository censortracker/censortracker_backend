from django.contrib import admin
from django.contrib import messages

from server.apps.core.models import Config, Country, CountryRegistry, ProxyConfig


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

    def make_active(self, request, queryset):
        queryset.update(active=True)
        messages.success(request, 'Done!')

    def make_inactive(self, request, queryset):
        queryset.update(active=False)
        messages.success(request, 'Done!')

    make_active.short_description = 'Mark selected as active'
    make_inactive.short_description = 'Mark selected as inactive'

    actions = ['make_active', 'make_inactive']


@admin.register(CountryRegistry)
class CountryRegistryAdmin(admin.ModelAdmin):
    pass
