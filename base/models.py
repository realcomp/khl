#coding: utf-8
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from picklefield.fields import PickledObjectField
from filer.fields.image import FilerImageField

from .choices import SOCIAL_NETWORKS
from .managers import SeasonQuerySet, IIFQuerySet


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
    title = models.CharField(_('Title from parser'), max_length=1024,
                                blank=True, editable=False)
    __unicode__ = lambda self: self.ru_title

    def save(self, **kwargs):
        if not self.ru_title and self.title:
            self.ru_title = self.title
        super(TitleBaseModel, self).save(**kwargs)

    class Meta:
        abstract=True


class Season(TitleBaseModel):
    objects = SeasonQuerySet.as_manager()
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)

    @property
    def short_title(self):
        return '%s/%s' % (
            str(self.start_date.year)[2:], str(self.end_date.year)[2:])

    @property
    def is_last(self):
        try:
            season = Season.objects.active().latest('end_date')
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


class InstagramUser(models.Model):
    instagram_id = models.CharField(_('Instagram ID'), max_length=1024)
    full_name = models.CharField(_('Full name'), max_length=1024, blank=True)
    profile_picture = models.URLField(_('Profile picture'), max_length=1024,
                                        blank=True)
    username = models.CharField(_('Username'), max_length=1024, blank=True)
    website = models.URLField(_('Website'), max_length=1024, blank=True)
    bio = models.TextField(_(b'BIO'), blank=True)
    class Meta:
        verbose_name = _('Instagram user')
        verbose_name_plural = _('Instagram users')


class InstagramImageFile(models.Model):
    objects = IIFQuerySet.as_manager()
    instagram_id = models.CharField(_('Instagram ID'), max_length=1024)
    link = models.URLField('Link')
    data = PickledObjectField()
    img = FilerImageField(verbose_name=_('Photo'))
    created = models.DateTimeField(_('Created date'), null=True, blank=True,)
    comment = models.CharField(_('Comment'), max_length=1024, blank=True)
    instagram_user = models.ForeignKey(InstagramUser, null=True)
    class Meta:
        verbose_name = _('Instagram image file')
        verbose_name_plural = _('Instagram image files')
        ordering = ('created', 'pk')
