# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from ..views.events import BirthdayEvent, MatchEvent


class EventSerializer(serializers.Serializer):
    date = serializers.DateField()
    title = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    url = serializers.URLField()
    image = serializers.URLField()

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
            return '%s - %s' % (home_team, guest_team)

    def get_type(self, event):
        if isinstance(event, BirthdayEvent):
            return _('Birth day')
        elif isinstance(event, MatchEvent):
            return _('Match')

    class Meta(object):
        fields = 'date', 'title', 'type', 'url', 'image'
