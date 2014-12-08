#coding: utf-8
from __future__ import unicode_literals
from django.db import models


class MatchManager(models.Manager):
    b''' Мененжер матчей по-умолчанию '''
    def create_match(self, **kwargs):
        b''' метод создания записи о матче '''
