# -*- coding: utf-8 -*-

from django.urls import path

from server.apps.api import views

urlpatterns = [
    path('domain/', views.DomainCreateAPIView.as_view(), name='create-domain'),
    path('domains/', views.DomainListView.as_view(), name='domain-list'),
]

app_name = 'api'
