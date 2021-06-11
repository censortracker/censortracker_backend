# -*- coding: utf-8 -*-

"""
Main URL mapping configuration file.

Include other URL сonfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from server.apps.api import urls as api_urls

urlpatterns = [
    path("dashboard/ad/", admin.site.urls),
    path("api/", include(api_urls, namespace="api")),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar
    from django.views.static import serve

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path("__debug__/", include(debug_toolbar.urls)),
        # Serving media files in development only:
        re_path(
            r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT,},
        ),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
