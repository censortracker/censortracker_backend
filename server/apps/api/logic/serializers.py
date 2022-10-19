from rest_framework import serializers

from server.apps.core.models import Config, Country, Ignore, ProxyConfig


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("name", "iso_a2_code", "locale_code")


# Keep this serializer for backward compatibility with the old API
class LegacyConfigSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source="country", read_only=True)

    class Meta:
        model = Config
        exclude = ("id", "country")


class ConfigSerializer(serializers.ModelSerializer):
    country_code = serializers.CharField(source="country.iso_a2_code", read_only=True)
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = Config
        exclude = ("id", "country")


class ProxyConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxyConfig
        exclude = ("id",)


class IgnoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ignore
        exclude = ("pk", "name")
