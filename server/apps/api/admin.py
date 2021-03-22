# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import Count

from server.apps.api.models import Domain, Case


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    pass

    list_display = ('domain', 'view_related_cases', 'cases_count')

    def get_queryset(self, request):
        """
        Make new '_cases_count' field to use it later for ordering and url-link-text
        """
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_cases_count=Count('cases', distinct=True))
        return queryset

    def cases_count(self, obj):
        return obj._cases_count

    def view_related_cases(self, obj):
        """
        Makes links to related case objects
        """
        count = obj._cases_count
        url = f'{reverse("admin:api_case_changelist")}?domain__id={obj.id}'
        return format_html(f'<a href={url}>{count} Related Cases</a>')

    cases_count.admin_order_field = '_cases_count'


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    pass

    list_display = ('domain', 'client_region', 'client_provider')
