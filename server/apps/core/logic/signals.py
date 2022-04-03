from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from server.apps.core.logic import actions
from server.apps.core.models import Ignore, ProxyConfig


@receiver([post_save, post_delete], sender=ProxyConfig)
def generate_api_proxy_configs(sender, instance, **kwargs):
    actions.update_api_proxy_configs()


@receiver([post_save, post_delete], sender=Ignore)
def generate_api_ignore_data(sender, instance, **kwargs):
    actions.update_api_ignore()
