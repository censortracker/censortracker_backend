from rest_framework import serializers

from server.apps.api.models import Domain


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('domain', 'client_ip')


class DomainListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('domain',)
