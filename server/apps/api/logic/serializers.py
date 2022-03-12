from rest_framework import serializers

from server.apps.api.models import Case, Domain
from server.apps.core.models import Config, Country, ProxyConfig


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ("domain", "client_ip", "client_country", "user_agent")


class DomainListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ("domain",)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("name", "iso_a2_code", "locale_code")


class ConfigSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source="country", read_only=True)

    class Meta:
        model = Config
        exclude = (
            "id",
            "country",
        )


class ProxyConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxyConfig
        exclude = ("id", "name", "pingHost", "pingPort", "priority")
