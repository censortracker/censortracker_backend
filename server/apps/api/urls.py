# -*- coding: utf-8 -*-

from django.urls import path

from server.apps.api import views

urlpatterns = [
    path("case/", views.CaseCreateAPIView.as_view(), name="create_case"),
    path("domains/", views.DomainListView.as_view(), name="domain_list"),
    path("config/", views.ConfigRetrieveAPIView.as_view(), name="config_detail"),
    path(
        "proxy-configs/", views.ProxyConfigListView.as_view(), name="proxy_config_list"
    ),
]

app_name = "api"
