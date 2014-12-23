# -*- coding: utf-8 -*-
from dateutil import relativedelta

from django.utils import timezone

from rest_framework import fields, serializers

from .models import Coach, Arena, Club, Player


class AbstractManSerializer(serializers.ModelSerializer):
    fio = serializers.SerializerMethodField()

    def get_fio(self, obj):
        # TODO: get current language
        language = 'ru'
        if hasattr(obj, '%s_fio' % language):
            return getattr(obj, '%s_fio' % language)
        return obj.en_fio


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
        fields = (
            'pk', 'fio')
        model = Coach


class ArenaSerializer(serializers.ModelSerializer):
    logo = fields.ReadOnlyField(source='photo.url')

    class Meta(object):
        fields = (
            'pk', 'logo')
        model = Arena


class ClubListSerializer(serializers.ModelSerializer):
    logo = fields.ReadOnlyField(source='logo.url')
    # address
    coach = CoachSerializer()
    arena = ArenaSerializer()
    # players
    # farm_club
    # junior_club

    class Meta(object):
        fields = (
            'pk', 'logo', 'site', 'contacts', 'coach', 'arena')
        model = Club


class ClubSerializer(ClubListSerializer):
    pass
