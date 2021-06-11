from django.contrib import admin

from server.apps.core.models import Config, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("country",)
