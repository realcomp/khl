# -*- coding: utf-8 -*-
from rest_framework import serializers

from . import LangDepSerializer, AbstractManSerializer
from ..models import Player, Timeline


class TimelineSerializer(LangDepSerializer):
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()
    headline = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    asset = serializers.SerializerMethodField()

    get_headline = lambda self, obj: self._get_field(obj, 'headline')
    get_text = lambda self, obj: self._get_field(obj, 'text')

    def _get_date(self, date):
        if date:
            return '%d,%d,%d' % (date.year, date.month, date.day)

    def get_startDate(self, obj):
        return self._get_date(obj.start_date)

    def get_endDate(self, obj):
        return self._get_date(obj.end_date)

    def get_asset(self, obj):
        return {
            'media': obj.media and obj.media.url,
            'thumbnail': obj.media and obj.media.url,
            'credit': self._get_field(obj, 'media_credit'),
            'caption': self._get_field(obj, 'media_caption'),
        }

    class Meta(object):
        fields = (
            'startDate', 'endDate', 'headline', 'text', 'tag', 'asset')
        model = Timeline


class PlayerTimelineSerializer(AbstractManSerializer):
    headline = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    asset = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    date = TimelineSerializer(many=True, source='timeline_set')

    def get_headline(self, obj):
        return ' '.join((
            self._get_field(obj, 'lastname'), self._get_field(obj, 'name')))

    def get_text(self, obj):
        return 'TEXT'

    def get_asset(self, obj):
        return {
            'media': obj.photo and obj.photo.url,
            'thumbnail': obj.photo and obj.photo.url,
        }

    def get_type(self, obj):
        return 'default'

    class Meta(object):
        fields = (
            'headline', 'text', 'asset', 'type', 'date')
        model = Player
