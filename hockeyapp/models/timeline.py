# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from base.models import LocaleAttrMixin


class Timeline(LocaleAttrMixin, models.Model):
    start_date = models.DateTimeField(_('Start date'), blank=True, null=True)
    end_date = models.DateTimeField(_('End date'), blank=True, null=True)
    ru_headline = models.CharField(
        _('Headline (RU)'), max_length=255, blank=True, null=True)
    en_headline = models.CharField(
        _('Headline (EN)'), max_length=255, blank=True, null=True)
    ru_text = models.TextField(_('Text (RU)'), blank=True, null=True)
    en_text = models.TextField(_('Text (EN)'), blank=True, null=True)
    media = FilerImageField(verbose_name=_('Media'), null=True, blank=True)
    ru_media_credit = models.CharField(
        _('Media credit (RU)'), max_length=255, blank=True, null=True)
    en_media_credit = models.CharField(
        _('Media credit (EN)'), max_length=255, blank=True, null=True)
    ru_media_caption = models.CharField(
        _('Media caption (RU)'), max_length=255, blank=True, null=True)
    en_media_caption = models.CharField(
        _('Media caption (EN)'), max_length=255, blank=True, null=True)
    type = models.CharField(
        _('Type'), max_length=255, blank=True, null=True)
    tag = models.CharField(
        _('Tag'), max_length=255, blank=True, null=True)

    # related objects
    player = models.ForeignKey(
        'hockeyapp.Player', verbose_name=_('Player'),
        on_delete=models.SET_NULL,
        blank=True, null=True)
    club = models.ForeignKey(
        'hockeyapp.Club', verbose_name=_('Club'), on_delete=models.SET_NULL,
        blank=True, null=True)

    class Meta(object):
        ordering = 'start_date',
        verbose_name = _('Timeline event')
        verbose_name_plural = _('Timeline events')
