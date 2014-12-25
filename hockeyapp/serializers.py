# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from dateutil import relativedelta

from django.utils import timezone

from rest_framework import fields, serializers

from .models import Coach, Arena, Club, Player


class LangDepSerializer(serializers.ModelSerializer):
    '''
    Language-Dependent Serializer
    '''
    def _get_field(self, obj, field_name):
        request = self.context['request']
        get_field_name = lambda lang: '%s_%s' % (lang, field_name)
        if hasattr(obj, get_field_name(request.LANGUAGE_CODE)):
            return getattr(obj, get_field_name(request.LANGUAGE_CODE))
        return getattr(obj, get_field_name('en'))


class AbstractManSerializer(LangDepSerializer):
    fio = serializers.SerializerMethodField()
    get_fio = lambda self, obj: self._get_field(obj, 'fio')


class TitleBaseSerializer(LangDepSerializer):
    title = serializers.SerializerMethodField()
    get_title = lambda self, obj: self._get_field(obj, 'title')


class PlayerCardSerializer(AbstractManSerializer):
    photo = fields.ReadOnlyField(source='photo.url')
    line = fields.ReadOnlyField(source='get_line_display')
    birth_date = serializers.SerializerMethodField()
    birth_date_short = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    khl_url = serializers.SerializerMethodField()

    def get_birth_date(self, obj):
        return obj.birth_date and obj.birth_date.strftime('%d %B %Y')

    def get_birth_date_short(self, obj):
        return obj.birth_date and obj.birth_date.strftime('%d.%m.%Y')

    def get_age(self, obj):
        if obj.birth_date:
            delta = relativedelta.relativedelta(
                timezone.now().date(), obj.birth_date)
            return delta.years, delta.months
        return None, None

    def get_khl_url(self, obj):
        return 'http://www.khl.ru/players/%s/' % obj.khl_id

    class Meta(object):
        fields = (
            'pk', 'fio', 'line', 'birth_date', 'age', 'weight', 'height',
            'photo', 'khl_url', 'birth_date_short')
        model = Player


class CoachSerializer(AbstractManSerializer):
    class Meta(object):
        fields = 'pk', 'fio'
        model = Coach


class ArenaSerializer(TitleBaseSerializer):
    photo = fields.ReadOnlyField(source='photo.url')

    class Meta(object):
        fields = 'pk', 'title', 'photo', 'capacity', 'site', 'contacts'
        model = Arena


class AddressSerializer(TitleBaseSerializer):
    class Meta(object):
        fields = 'pk', 'title'
        model = Arena


class ClubListSerializer(TitleBaseSerializer):
    logo = fields.ReadOnlyField(source='logo.url')
    coach = CoachSerializer()
    arena = ArenaSerializer()
    # players
    # farm_club
    # junior_club
    current_address = AddressSerializer()

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'site', 'contacts', 'coach', 'arena',
            'current_address')
        model = Club


class ClubSerializer(ClubListSerializer):
    pass
