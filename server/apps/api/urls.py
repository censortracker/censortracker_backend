# -*- coding: utf-8 -*-

from django.urls import path

from server.apps.api import views

urlpatterns = [
    path("case/", views.CaseCreateAPIView.as_view(), name="create_case"),
    path("port/", views.UpdatePortAPIView.as_view(), name="update_port"),
    path("domains/", views.DomainListView.as_view(), name="domain_list"),
    path("countries/", views.CountryListView.as_view(), name="country_list"),
    path("config/", views.ConfigRetrieveAPIView.as_view(), name="config_detail"),
]

app_name = "api"
