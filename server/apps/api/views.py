# -*- coding: utf-8 -*-

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from server.apps.api.logic.mixins import ClientIPMixin
from server.apps.api.logic.permissions import AllowByHeaders
from server.apps.api.logic.serializers import (DomainListSerializer,
                                               CaseSerializer)
from server.apps.api.models import Domain


class CaseCreateAPIView(ClientIPMixin, generics.CreateAPIView):
    serializer_class = CaseSerializer
    permission_classes = [AllowByHeaders]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['client_ip'] = self.get_client_ip(request)
        data['domain'] = self.get_domain_or_create(data)
        serializer = self.serializer_class(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 200, 'message': 'OK'})
        except ValidationError:
            return Response({"errors": (serializer.errors,)},
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_domain_or_create(data):
        domain_name = data.get('domain', '').lower()
        if not domain_name:
            return
        domain, created = Domain.objects.get_or_create(domain=domain_name)
        return domain.pk


class DomainListView(generics.ListAPIView):
    serializer_class = DomainListSerializer
    permission_classes = [AllowAny]
    queryset = Domain.objects.all()
