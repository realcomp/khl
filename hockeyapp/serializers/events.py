# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from ..views.events import (
    BirthdayEvent, MatchEvent, GuestMatchEvent, TimelineEvent)


class EventSerializer(serializers.Serializer):
    date = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    url = serializers.URLField()
    image = serializers.URLField()
    rgb = serializers.ReadOnlyField()
    logos = serializers.ReadOnlyField()
    logos_urls = serializers.ReadOnlyField()

    def get_date(self, event):
        return event.date.strftime('%Y-%m-%dT%H:%M%Z')

    def get_type(self, event):
        request = self.context.get('request')
        if isinstance(event, BirthdayEvent):
            return '%s: %s %s' % (_('Birthday'), event.obj.age[0], _('years'))
        elif isinstance(event, MatchEvent):
            return _('Match')
        elif isinstance(event, TimelineEvent):
            return event.obj.get_locale_attr('headline', request=request)

    def get_title(self, event):
        request = self.context.get('request')
        if isinstance(event, BirthdayEvent):
            name = event.obj.get_locale_attr('name', request=request)
            lastname = event.obj.get_locale_attr('lastname', request=request)
            return '%s %s' % (lastname, name)
        elif isinstance(event, MatchEvent):
            home_team = event.obj.home_team.get_locale_attr(
                'title', request=request)
            guest_team = event.obj.guest_team.get_locale_attr(
                'title', request=request)
            teams = [home_team, guest_team]
            if isinstance(event, GuestMatchEvent):
                teams.reverse()
            return '{} - {}'.format(*teams)
        elif isinstance(event, TimelineEvent):
            name = event.obj.player.get_locale_attr('name', request=request)
            lastname = event.obj.player.get_locale_attr('lastname', request=request)
            return '%s %s' % (lastname, name)

    class Meta(object):
        fields = (
            'date', 'title', 'type', 'url', 'image', 'logos', 'logos_urls',
            'rgb')
