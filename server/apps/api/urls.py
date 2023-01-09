# -*- coding: utf-8 -*-

from django.urls import path

from server.apps.api import views

urlpatterns = [
    path("countries/", views.CountryListView.as_view(), name="country_list"),
    path("config/", views.ConfigRetrieveAPIView.as_view(), name="config_detail"),
    path(
        "config/<str:country_code>/",
        views.ConfigRetrieveAPIView.as_view(),
        name="config_detail",
    ),
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
    path(
        "proxy-list/",
        views.ProxyConfigListView.as_view(),
        name="proxy_list",
    ),
]

app_name = "api"
