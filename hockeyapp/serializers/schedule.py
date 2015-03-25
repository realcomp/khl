# -*- coding: utf-8 -*-
from rest_framework import serializers

from . import (
    CountrySerializer, AddressSerializer, ArenaSerializer,
    ClubLightListSerializer)
from ..models import Arena, Schedule


class ScheduleArenaSerializer(ArenaSerializer):
    address = AddressSerializer()
    country = CountrySerializer()

    class Meta(object):
        fields = (
            'pk', 'title', 'photo', 'capacity', 'site', 'contacts', 'url',
            'coords', 'en_title', 'address', 'country')
        model = Arena


class ScheduleSerializer(serializers.ModelSerializer):
    arena = ScheduleArenaSerializer()
    team = serializers.SerializerMethodField()

    def get_team(self, obj):
        request = self.context.get('request')
        if request and 'is_home' in request.GET:
            return ClubLightListSerializer(
                obj.guest_team, context=self.context).data
        if request and 'is_guest' in request.GET:
            return ClubLightListSerializer(
                obj.home_team, context=self.context).data

    class Meta(object):
        fields = (
            'pk', 'date', 'arena', 'team')
        model = Schedule
