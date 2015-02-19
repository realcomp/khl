from __future__ import absolute_import

import os

import celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportomatics.settings')


class Celery(celery.Celery):
    def on_configure(self):
        import raven
        from raven.contrib.celery import register_signal, register_logger_signal
        if hasattr(settings, 'RAVEN_CONFIG'):
            client = raven.Client(dsn=settings.RAVEN_CONFIG.get('dsn'))
        else:
            client = raven.Client()            
        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)
        # hook into the Celery error handler
        register_signal(client)


app = Celery(__name__, backend='redis')        
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

local_celery_crontab = crontab

#@app.task(bind=True)
#def debug_task(self):
    #print('Request: {0!r}'.format(self.request))