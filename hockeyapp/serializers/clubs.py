# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator

from rest_framework import serializers

from base.models import Season

from . import (
    SeasonSerializer,
    BasePlayerCardSerializer,
    BaseClubSerializer, ClubLightListSerializer,
    CoachSerializer)
from ..models import Club, ClubPlayer, Coach, Player


class ClubPlayerSerializer(BasePlayerCardSerializer):
    line_display = serializers.ReadOnlyField(source='get_line_display')
    club = ClubLightListSerializer()
    photo = serializers.ReadOnlyField(source='photo.url')
    is_joined = serializers.ReadOnlyField()
    is_left = serializers.ReadOnlyField()

    class Meta(object):
        fields = (
            'pk', 'fio', 'line', 'line_display', 'club', 'photo', 'number',
            'birth_date', 'birth_date_short', 'contract_type', 'age', 'url',
            'name', 'lastname', 'is_joined', 'is_left', 'is_legionnaire')
        model = Player


class ClubCoachSerializer(CoachSerializer):
    is_joined = serializers.ReadOnlyField()
    is_left = serializers.ReadOnlyField()

    class Meta(object):
        fields = 'pk', 'fio', 'name', 'lastname', 'is_joined', 'is_left'
        model = Player


class BaseClubTeamSerializer(BaseClubSerializer):
    season = serializers.SerializerMethodField()
    prev_season = serializers.SerializerMethodField()

    _seasons_selected = None
    _players = None
    _coaches = None

    def _get_seasons(self, obj):
        if not self._seasons_selected:
            request = self.context.get('request')
            try:
                season = obj.seasons.get(pk=request.GET.get('season'))
            except Season.DoesNotExist:
                season = obj.seasons[0]
            self._seasons_selected = (
                obj.get_prev_season(season) or season,
                season,
                obj.get_next_season(season) or season,
            )
        return self._seasons_selected

    def _get_players(self, obj):
        if self._players:
            return self._players
        clubplayers = map(
            lambda x: obj.clubplayer_set.filter(season=x),
            self._get_seasons(obj))
        players = map(
            lambda x: set(Player.objects.filter(clubplayer__in=x)),
            clubplayers)
        joined = players[1] - players[0]  # joined club in current season
        left = players[1] - players[2]  # left club in next season
        self._players = players[1]  # middle one is the current season
        for player in self._players:
            player.is_joined = player in joined
            player.is_left = player in left
        return self._players

    def _get_coaches(self, obj):
        if self._coaches:
            return self._coaches
        clubcoaches = map(
            lambda x: obj.coachclub_set.filter(season=x),
            self._get_seasons(obj))
        coaches = map(
            lambda x: set(Coach.objects.filter(coachclub__in=x)),
            clubcoaches)
        joined = coaches[1] - coaches[0]  # joined club in current season
        left = coaches[1] - coaches[2]  # left club in next season
        self._coaches = coaches[1]  # middle one is the current season
        for coach in self._coaches:
            coach.is_joined = coach in joined
            coach.is_left = coach in left
        return self._coaches

    def get_season(self, obj):
        return SeasonSerializer(
            self._get_seasons(obj)[1], context=self.context).data

    def get_prev_season(self, obj):
        seasons = self._get_seasons(obj)
        season = None
        if seasons[0].pk != seasons[1].pk:
            season = seasons[0]
        return SeasonSerializer(season, context=self.context).data


class ClubTeamSerializer(BaseClubTeamSerializer):
    seasons = SeasonSerializer(many=True)
    all_players = serializers.SerializerMethodField()
    offender_players = serializers.SerializerMethodField()
    defender_players = serializers.SerializerMethodField()
    goalkeeper_players = serializers.SerializerMethodField()
    coaches = serializers.SerializerMethodField()

    def get_all_players(self, obj):
        players = self._get_players(obj)
        return ClubPlayerSerializer(
            players, context=self.context, many=True).data

    def get_offender_players(self, obj):
        players = filter(lambda x: x.line == 3, self._get_players(obj))
        return ClubPlayerSerializer(
            players, context=self.context, many=True).data

    def get_defender_players(self, obj):
        players = filter(lambda x: x.line == 2, self._get_players(obj))
        return ClubPlayerSerializer(
            players, context=self.context, many=True).data

    def get_goalkeeper_players(self, obj):
        players = filter(lambda x: x.line == 1, self._get_players(obj))
        return ClubPlayerSerializer(
            players, context=self.context, many=True).data

    def get_coaches(self, obj):
        coaches = self._get_coaches(obj)
        return ClubCoachSerializer(
            coaches, context=self.context, many=True).data

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'site', 'contacts', 'coach', 'arena',
            'address', 'all_players', 'offender_players',
            'defender_players', 'goalkeeper_players', 'coaches',
            'url', 'seasons', 'season', 'prev_season')
        model = Club


class ClubTeamCompareSerializer(BaseClubTeamSerializer):
    clubs = serializers.SerializerMethodField()

    def _get_clubs(self, obj):
        current_players = self._get_players(obj)
        season = self._get_seasons(obj)[0]  # previous season
        clubplayers = (
            ClubPlayer.objects
            .filter(player__in=current_players, season=season)
            .order_by('club'))
        # we need duplicates
        return map(operator.attrgetter('club'), clubplayers)

    def get_clubs(self, obj):
        clubs = self._get_clubs(obj)
        return ClubLightListSerializer(
            clubs, context=self.context, many=True).data

    class Meta(object):
        fields = (
            'pk', 'title', 'site', 'contacts', 'logo', 'url', 'season',
            'prev_season', 'clubs')
        model = Club
