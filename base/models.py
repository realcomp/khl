#coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _


class LocaleAttrMixin(object):
    def get_locale_attr(self, attr, request=None):
        cd = 'ru'
        if request and request.LANGUAGE_CODE:
            cd = request.LANGUAGE_CODE
        _attr = hasattr(self, cd+'_'+attr) and getattr(self, cd+'_'+attr)
        return _attr or hasattr(self, attr) and getattr(self, attr)
        

class TitleBaseModel(models.Model):
    ru_title = models.CharField(_('Title (rus)'), max_length=1024, blank=True)
    en_title = models.CharField(_('Title (en)'), max_length=1024, blank=True)
    __unicode__ = lambda self: self.ru_title
    class Meta:
        abstract=True