#coding: utf-8
from __future__ import unicode_literals
from django.db import models


class TitleBaseModel(models.Model):
    title = models.CharField(b'Название', max_length=1024, blank=True)
    __unicode__ = lambda self: self.title
    class Meta:
        abstract=True


class Region(TitleBaseModel):
    class Meta:
        verbose_name=b'Регион'
        verbose_name_plural=b'Регионы'