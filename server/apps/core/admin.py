from django.contrib import admin

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
        "priority",
        "active",
    )


@admin.register(CountryRegistry)
class CountryRegistryAdmin(admin.ModelAdmin):
    pass
