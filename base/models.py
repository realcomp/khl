#coding: utf-8
from __future__ import unicode_literals

import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .choices import SOCIAL_NETWORKS
from .managers import SeasonManager


class LocaleAttrMixin(object):
    def get_locale_attr(self, attr, request=None):
        cd = 'ru'
        if request and request.LANGUAGE_CODE:
            cd = request.LANGUAGE_CODE
        if hasattr(self, '%s_%s' % (cd, attr)):
            return getattr(self, '%s_%s' % (cd, attr))
        elif getattr(self, '%s_%s' % ('ru', attr)):
            return getattr(self, '%s_%s' % ('ru', attr))
        return getattr(self, attr)


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

    @property
    def short_title(self):
        return '%s/%s' % (
            str(self.start_date.year)[2:], str(self.end_date.year)[2:])

    @property
    def is_last(self):
        try:
            season = (
                Season.objects
                .filter(start_date__lte=datetime.datetime.now().date())
                .latest('end_date'))
            return self.pk == season.pk
        except Season.DoesNotExist:
            return False


class TitleAlias(TitleBaseModel):
    b''' Общая модель алиасов названий '''
    class Meta:
        verbose_name = _('Title alias')
        verbose_name_plural = _('Title aliases')


class SocialAbstract(TitleBaseModel):
    url = models.URLField('URL', blank=True)
    stype = models.PositiveIntegerField(_('Social Network'), null=True,
                                        choices = SOCIAL_NETWORKS)
    __unicode__ = lambda self: '{}: {}'.format(self.stype, self.url)
    class Meta:
        abstract=True

class SocialNetValue(SocialAbstract):
    class Meta:
        verbose_name = _('Social Network Value')
        verbose_name_plural = _('Social Network Values')
