from rest_framework import serializers

from server.apps.api.models import Case, Domain


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ('domain', 'client_ip')


class DomainListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('domain',)
