#coding: utf-8
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import SeasonManager


class LocaleAttrMixin(object):
    def get_locale_attr(self, attr, request=None):
        cd = 'ru'
        if request and request.LANGUAGE_CODE:
            cd = request.LANGUAGE_CODE
        _attr = hasattr(self, cd+'_'+attr) and getattr(self, cd+'_'+attr)
        return _attr or hasattr(self, attr) and getattr(self, attr)


class AdminLinkMixin(object):
    def admin_change_link(self):
        if self.pk:
            info = (self._meta.app_label, self._meta.module_name)
            return reverse("admin:%s_%s_change" % info, args=[self.pk])

    @classmethod
    def admin_list_link(cls):
        return reverse("admin:{}_{}_changelist".format( cls._meta.app_label,
                                                        cls._meta.module_name))


class TitleBaseModel(LocaleAttrMixin, models.Model):
    ru_title = models.CharField(_('Title (rus)'), max_length=1024, blank=True)
    en_title = models.CharField(_('Title (en)'), max_length=1024, blank=True)
    __unicode__ = lambda self: self.ru_title
    class Meta:
        abstract=True


class Season(TitleBaseModel):
    objects = SeasonManager()
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)
