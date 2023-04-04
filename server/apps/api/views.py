# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_api_key.permissions import HasAPIKey

from server.apps.api.logic.mixins import ClientIPMixin
from server.apps.api.logic.serializers import (
    CountrySerializer,
    LegacyConfigSerializer,
    ProxyConfigSerializer,
)
from server.apps.core.models import Config, Country, ProxyConfig


class ProxyConfigCreateAPIView(generics.CreateAPIView):
    queryset = ProxyConfig.objects.all()
    permission_classes = (HasAPIKey,)
    serializer_class = ProxyConfigSerializer


class ProxyConfigUpdateAPIView(generics.UpdateAPIView):
    lookup_field = "name"
    queryset = ProxyConfig.objects.all()
    permission_classes = (HasAPIKey,)
    serializer_class = ProxyConfigSerializer


class ConfigRetrieveAPIView(ClientIPMixin, generics.RetrieveAPIView):
    serializer_class = LegacyConfigSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        country_code = self.kwargs.get("country_code")
        if not country_code:
            country_code = self.get_client_country_code()
        return get_object_or_404(Config, country__iso_a2_code__iexact=country_code)


class CountryListView(generics.ListAPIView):
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    queryset = Country.objects.filter(active=True)


class ProxyConfigListView(generics.ListAPIView):
    serializer_class = ProxyConfigSerializer
    permission_classes = [AllowAny]
    queryset = ProxyConfig.objects.order_by("-weight", "-name")
