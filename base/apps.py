#coding: utf-8
from __future__ import unicode_literals
from django.apps import AppConfig


class BaseAppConfig(AppConfig):
    name = 'base'
    verbose_name = u'Общее'