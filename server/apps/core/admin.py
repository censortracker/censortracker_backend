from django.contrib import admin

from server.apps.core.models import Config, Country, ProxyConfig, CountryRegistry


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("country",)


@admin.register(ProxyConfig)
class ProxyConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "server", "priority")


@admin.register(CountryRegistry)
class CountryRegistryAdmin(admin.ModelAdmin):
    pass
