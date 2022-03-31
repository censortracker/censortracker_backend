# -*- coding: utf-8 -*-

from django.urls import path

from server.apps.api import views

urlpatterns = [
    path("case/", views.CaseCreateAPIView.as_view(), name="create_case"),
    path("domains/", views.DomainListView.as_view(), name="domain_list"),
    path("countries/", views.CountryListView.as_view(), name="country_list"),
    path("config/", views.ConfigRetrieveAPIView.as_view(), name="config_detail"),
    path(
        "proxy/update/<str:name>/",
        views.ProxyConfigUpdateAPIView.as_view(),
        name="proxy_update",
    ),
    path(
        "proxy/create/",
        views.ProxyConfigCreateAPIView.as_view(),
        name="proxy_create",
    ),
]

app_name = "api"
