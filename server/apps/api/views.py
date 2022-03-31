# -*- coding: utf-8 -*-

import validators
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from server.apps.api.logic.mixins import ClientIPMixin
from server.apps.api.logic.serializers import (
    CaseSerializer,
    ConfigSerializer,
    CountrySerializer,
    DomainListSerializer,
)
from server.apps.api.logic.throttling import (
    ConfigRetrieveRateThrottle,
    CountryListRateThrottle,
    CreateCaseRateThrottle,
    DomainListRateThrottle,
)
from server.apps.api.models import Domain
from server.apps.core.models import Config, Country, ProxyConfig


# TODO: Refactor


class ToggleProxyConfigAPIView(generics.UpdateAPIView):
    permission_classes = [HasAPIKey]

    def patch(self, request, *args, **kwargs) -> Response:
        name = request.data.get("name")
        active = request.data.get("active")

        try:
            pc = ProxyConfig.objects.get(name__iexact=name)
            pc.active = active
            pc.save()
            return Response(
                {"success": "ok", "name": pc.name}, status=status.HTTP_200_OK
            )
        except ProxyConfig.DoesNotExist:
            return Response(
                {"error": "such server does not exist"}, status=status.HTTP_200_OK
            )
        except BaseException as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdatePortAPIView(generics.UpdateAPIView):
    permission_classes = [HasAPIKey]

    def patch(self, request, *args, **kwargs) -> Response:
        name = request.data.get("name")
        port = request.data.get("port")
        ping_port = request.data.get("ping_port")

        try:
            pc = ProxyConfig.objects.get(name__iexact=name)
            pc.port = port
            pc.ping_port = ping_port
            pc.save()
            return Response({"success": "ok"}, status=status.HTTP_200_OK)
        except ProxyConfig.DoesNotExist:
            return Response(
                {"error": "such server does not exist"}, status=status.HTTP_200_OK
            )
        except BaseException as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CaseCreateAPIView(ClientIPMixin, generics.CreateAPIView):
    serializer_class = CaseSerializer
    permission_classes = [AllowAny]
    throttle_classes = [CreateCaseRateThrottle]

    def create(self, request, *args, **kwargs) -> Response:
        domain = request.data.get("domain")
        hostname = request.data.get("hostname")
        user_agent = request.data.get("userAgent")

        if not domain:
            domain = hostname

        if not domain or not validators.domain(domain):
            return Response(
                {"error": "Domain is empty or invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        domain_obj, _ = Domain.objects.get_or_create(domain=domain)
        request.data["domain"] = domain_obj.pk
        request.data["client_ip"] = self.get_client_ip()

        if user_agent:
            request.data["user_agent"] = user_agent

        try:
            request.data["client_country"] = Country.objects.get(
                iso_a2_code=self.get_client_country_code()
            ).pk
        except Country.DoesNotExist:
            pass

        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": status.HTTP_201_CREATED, "message": "created"})
        except ValidationError:
            return Response(
                {"errors": (serializer.errors,)}, status=status.HTTP_400_BAD_REQUEST
            )


class DomainListView(generics.ListAPIView):
    serializer_class = DomainListSerializer
    permission_classes = [AllowAny]
    throttle_classes = [DomainListRateThrottle]
    queryset = Domain.objects.distinct()

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset().order_by("-domain")
        serializer = DomainListSerializer(queryset, many=True)
        return Response([i["domain"] for i in serializer.data])


class ConfigRetrieveAPIView(ClientIPMixin, generics.RetrieveAPIView):
    serializer_class = ConfigSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ConfigRetrieveRateThrottle]

    def get_object(self):
        country_code = self.get_client_country_code()
        return get_object_or_404(Config, country__iso_a2_code__iexact=country_code)


class CountryListView(generics.ListAPIView):
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    throttle_classes = [CountryListRateThrottle]
    queryset = Country.objects.filter(active=True)
