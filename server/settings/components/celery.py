# -*- coding: utf-8 -*-

"""
Celery module
"""

from server.settings.components import env, secret

CELERY_BROKER_URL = 'amqp://{user}:{passwd}@{host}/{app}'.format(
    user=secret('user', stack_name='rbt', default='guest'),
    passwd=secret('passwd', stack_name='rbt', default='guest'),
    host=env('RABBIT_HOST'),
    app=env('RABBIT_APP', default=''),
)
