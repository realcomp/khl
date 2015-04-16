# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from rest_framework import pagination, serializers
from api.addresses.serializers import AddressMinimalSerializer, CountrySerializer
from api.base.serializers import IIFMinimalSerializer, FIFSerialiser
from api.base.serializers import TitleBaseSerializer, LangDepSerializer
from api.base.serializers import SeasonSerializer

from hockeyapp.models import ArenaInstaPhoto, Club, Match, Player, Arena

from hockeyapp.serializers import CoachSerializer, LeagueSerializer


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
        fields = (  'id', 'number', 'line', 'ru_fio', 'photo', 'fio', 'name', 'lastname')
        read_only_fields = fields


class ArenaClubListSerializer(TitleBaseSerializer):
    url = drf.serializers.ReadOnlyField(source='get_absolute_url')
    class Meta(object):
        fields = 'pk', 'title', 'url', 'coords', 'contacts'
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


class ClubListPaginationSerializer(pagination.PaginationSerializer):
    leagues = serializers.SerializerMethodField()
    league = serializers.SerializerMethodField()

    def get_leagues(self, page):
        view = self.context.get('view')
        return LeagueSerializer(
            view._get_leagues(), context=self.context, many=True).data

    def get_league(self, page):
        view = self.context.get('view')
        return LeagueSerializer(
            view._get_league(), context=self.context).data


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


class I18NClubMinimalSerialiser(TitleBaseSerializer):
    title_verbose = drf.serializers.SerializerMethodField()
    def get_title_verbose(self, obj):
        return obj.get_title_verbose(request=self.context.get('request'))
    logo = drf.serializers.ReadOnlyField(source='logo.url')
    url = drf.serializers.ReadOnlyField(source='get_absolute_url')
    address = AddressMinimalSerializer()
    class Meta:
        model = Club
        fields = 'id', 'title_verbose', 'url', 'logo', 'address', 'title'


class MatchListSerializer(drf.serializers.ModelSerializer):
    arena_capacity = drf.serializers.SerializerMethodField()
    opponent = drf.serializers.SerializerMethodField()
    score = drf.serializers.SerializerMethodField()
    opponent_score = drf.serializers.SerializerMethodField()
    is_home = drf.serializers.SerializerMethodField()

    def _get_club_id(self):
        _request = self.context.get('request')
        if _request and _request.GET.get('club'):
            return int(_request.GET.get('club'))

    def get_arena_capacity(self, obj):
        view = self.context.get('view')
        if view and view.club_arena_capacity:
            return view.club_arena_capacity

    def get_opponent(self, obj):
        club_id = self._get_club_id()
        if club_id:
            if obj.guest_team.pk == club_id:
                team = obj.home_team
            else:
                team = obj.guest_team
            return I18NClubMinimalSerialiser(team,context=self.context).data

    def get_opponent_score(self, obj):
        club_id = self._get_club_id()
        if club_id:
            if obj.guest_team.pk == club_id:
                return obj.home_score
            else:
                return obj.guest_score

    def get_score(self, obj):
        club_id = self._get_club_id()
        if club_id:
            if obj.guest_team.pk == club_id:
                return obj.guest_score
            else:
                return obj.home_score

    def get_is_home(self, obj):
        club_id = self._get_club_id()
        if club_id:
            return obj.home_team.pk == club_id

    class Meta:
        model = Match
        fields = (  'id', 'date', 'overtime_win', 'bullet_win', 'opponent',
                    'score', 'opponent_score', 'is_home', 'spectators',
                    'arena_capacity')