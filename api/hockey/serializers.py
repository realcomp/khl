# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from api.addresses.serializers import AddressMinimalSerializer
from api.base.serializers import IIFMinimalSerializer, FIFSerialiser
from api.base.serializers import TitleBaseSerializer
from hockeyapp.models import ArenaInstaPhoto, Club, Match, Player, Arena
from hockeyapp.serializers import CoachSerializer


class ArenaMinimalSerialiser(drf.serializers.ModelSerializer):
    class Meta:
        model = Arena
        fields = 'id', 'ru_title', 'club_set'
        read_only_fields = fields


class ClubMinimalSerialiser(drf.serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = 'id', 'ru_title', 'get_absolute_url', 'arena'
        read_only_fields = fields


class ArenaInstaPhotoSerializer(drf.serializers.ModelSerializer):
    photo = IIFMinimalSerializer()
    players = drf.serializers.PrimaryKeyRelatedField(many=True, read_only=False,
            allow_null=True, queryset=Player.objects.all()
    )
    class Meta:
        model = ArenaInstaPhoto
        read_only_fields = 'photo',


class MatchMinimalSerialiser(drf.serializers.ModelSerializer):
    home_team = ClubMinimalSerialiser()
    guest_team = ClubMinimalSerialiser()
    class Meta:
        model = Match
        fields = 'id', 'home_team', 'guest_team', 'count', 'date'
        read_only_fields = fields


class PlayerMinimalSerialiser(drf.serializers.ModelSerializer):
    photo = FIFSerialiser()
    class Meta:
        model = Player
        fields = 'id', 'number', 'line', 'ru_fio', 'photo'
        read_only_fields = fields


class ArenaClubListSerializer(TitleBaseSerializer):
    url = drf.serializers.ReadOnlyField(source='get_absolute_url')
    class Meta(object):
        fields = 'pk', 'title', 'url',
        model = Arena


class ClubListSerializer(TitleBaseSerializer):
    title_verbose = drf.serializers.SerializerMethodField()
    def get_title_verbose(self, obj):
        return obj.get_title_verbose(request=self.context.get('request'))
    url = drf.serializers.ReadOnlyField(source="get_absolute_url")
    address = AddressMinimalSerializer()
    arena = ArenaClubListSerializer()
    coach = CoachSerializer()

    class Meta(object):
        fields = (
            'pk', 'title', 'title_verbose', 'logo', 'url',
            'address', 'arena', 'coach',)
        model = Club