# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from ..views.events import BirthdayEvent, MatchEvent, GuestMatchEvent


class EventSerializer(serializers.Serializer):
    date = serializers.DateField()
    title = serializers.SerializerMethodField()
    type = serializers.CharField()
    url = serializers.URLField()
    image = serializers.URLField()
    logos = serializers.ReadOnlyField()

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

    class Meta(object):
        fields = 'date', 'title', 'type', 'url', 'image', 'logos'
