# -*- coding: utf-8 -*-

from django.urls import path

from server.apps.api import views

urlpatterns = [
    path('case/', views.CaseCreateAPIView.as_view(), name='create-case'),
    path('domains/', views.DomainListView.as_view(), name='domain-list'),
]

app_name = 'api'
