# -*- coding: utf-8 -*-

from django.urls import path

from .views import IndexTemplate

urlpatterns = [path("", IndexTemplate.as_view(), name="index")]

app_name = "core"
