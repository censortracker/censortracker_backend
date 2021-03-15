# -*- coding: utf-8 -*-

"""
Main URL mapping configuration file.

Include other URL сonfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.contrib import admin
from django.urls import include, path

from server.apps.api import urls as api_urls


urlpatterns = [
    path("dashboard/ad/", admin.site.urls),
    path('api/', include(api_urls, namespace='api')),
]
