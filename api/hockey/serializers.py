# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from rest_framework import serializers
from api.addresses.serializers import AddressMinimalSerializer, CountrySerializer
from api.base.serializers import IIFMinimalSerializer, FIFSerialiser
from api.base.serializers import TitleBaseSerializer, LangDepSerializer
from api.base.serializers import SeasonSerializer

from hockeyapp.models import ArenaInstaPhoto, Club, Match, Player, Arena
from hockeyapp.serializers import CoachSerializer


class AbstractManSerializer(LangDepSerializer):
    fio = drf.serializers.SerializerMethodField()
    name = drf.serializers.SerializerMethodField()
    lastname = drf.serializers.SerializerMethodField()
    get_fio = lambda self, obj: self._get_field(obj, 'fio')
    get_name = lambda self, obj: self._get_field(obj, 'name')
    get_lastname = lambda self, obj: self._get_field(obj, 'lastname')


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


class PlayerMinimalSerialiser(AbstractManSerializer):
    photo = FIFSerialiser()
    class Meta:
        model = Player
        fields = (  'id', 'number', 'line', 'ru_fio', 'photo', 'fio')
        read_only_fields = fields


class ArenaClubListSerializer(TitleBaseSerializer):
    url = drf.serializers.ReadOnlyField(source='get_absolute_url')
    class Meta(object):
        fields = 'pk', 'title', 'url', 'coords'
        model = Arena


class ClubListSerializer(TitleBaseSerializer):
    title_verbose = drf.serializers.SerializerMethodField()
    def get_title_verbose(self, obj):
        return obj.get_title_verbose(request=self.context.get('request'))
    logo = drf.serializers.ReadOnlyField(source='logo.url')
    url = drf.serializers.ReadOnlyField(source='get_absolute_url')
    address = AddressMinimalSerializer()
    arena = ArenaClubListSerializer()
    coach = CoachSerializer()

    class Meta(object):
        fields = (
            'pk', 'title', 'title_verbose', 'logo', 'url',
            'address', 'arena', 'coach',)
        model = Club


class PartnerPlayerSerializer(PlayerMinimalSerialiser):
    citizenship = CountrySerializer()
    line_display = serializers.ReadOnlyField(source='get_line_display')

    class Meta:
        model = Player
        fields = (  'id', 'number', 'line', 'ru_fio', 'photo', 'fio', 'name', 
                    'lastname', 'citizenship', 'line_display')
        read_only_fields = fields


class PlayerPartnersBySeasonCount(drf.serializers.Serializer):
    seasons_count = drf.serializers.SerializerMethodField()
    get_seasons_count = lambda self, event: event[0]
    players = drf.serializers.SerializerMethodField()

    def get_players(self, event):
        return PartnerPlayerSerializer( event[1], context=self.context,
                                        many=True).data

    class Meta(object):
        fields = 'seasons_count', 'players',


class PlayerPartnersBySeason(drf.serializers.Serializer):
    season = drf.serializers.SerializerMethodField()

    def get_season(self, event):
        return SeasonSerializer(event[0], context=self.context).data

    players = drf.serializers.SerializerMethodField()

    def get_players(self, event):
        return PartnerPlayerSerializer( event[1], context=self.context,
                                        many=True).data

    class Meta(object):
        fields = 'season', 'players',