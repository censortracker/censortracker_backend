from django.db import models


class CaseManager(models.Manager):
    def unreported(self):
        return super().get_queryset().filter(reported=False)


class ProxyConfigManager(models.Manager):
    def active(self):
        return super().get_queryset().filter(active=True)
