from rest_framework import serializers

from server.apps.api.models import Case, Domain
from server.apps.core.models import Country, Config


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ("domain", "client_ip")


class DomainListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ("domain",)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("name", "iso_a3_code")


class ConfigSerializer(serializers.ModelSerializer):
    region = CountrySerializer(source="country", read_only=True)

    class Meta:
        model = Config
        exclude = ("country",)
