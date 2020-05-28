# -*- coding: utf-8 -*-

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from server.apps.api.logic.mixins import ClientIPMixin
from server.apps.api.logic.permissions import AllowByHeaders
from server.apps.api.logic.serializers import (DomainListSerializer,
                                               DomainSerializer)
from server.apps.api.models import Domain


class DomainCreateAPIView(ClientIPMixin, generics.CreateAPIView):
    serializer_class = DomainSerializer
    permission_classes = [AllowByHeaders]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['client_ip'] = self.get_client_ip(request)
        serializer = self.serializer_class(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 200, 'message': 'OK'})
        except ValidationError:
            return Response({"errors": (serializer.errors,)},
                            status=status.HTTP_400_BAD_REQUEST)


class DomainListView(generics.ListAPIView):
    serializer_class = DomainListSerializer
    permission_classes = [AllowAny]
    queryset = Domain.objects.all()
