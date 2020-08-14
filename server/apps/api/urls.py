# -*- coding: utf-8 -*-

from django.urls import path

from server.apps.api import views

urlpatterns = [
    path('case/', views.CaseCreateAPIView.as_view(), name='create_case'),
    path('domains/', views.DomainListView.as_view(), name='domain_list'),
]

app_name = 'api'
