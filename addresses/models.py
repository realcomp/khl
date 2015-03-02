#coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import TitleBaseModel


class Country(TitleBaseModel):
    class Meta:
        verbose_name=_('Country')
        verbose_name_plural=_('Countries')


class District(TitleBaseModel):
    class Meta:
        verbose_name=_('District')
        verbose_name_plural=_('Districts')


class City(TitleBaseModel):
    country = models.ForeignKey(Country, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True)

    class Meta:
        verbose_name=_('City')
        verbose_name_plural=_('Cities')


class Address(TitleBaseModel):
    city = models.ForeignKey(City, null=True, blank=True)
    ru_description = models.TextField(_('Description (rus)'), blank=True)
    en_description = models.TextField(_('Description (en)'), blank=True)

    class Meta:
        verbose_name=_('Address')
        verbose_name_plural=_('Addresses')
        ordering = ('ru_title', 'en_title', 'title', 'pk')
