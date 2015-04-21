# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from rest_framework import pagination, response, serializers

from api.addresses.serializers import AddressSerializer
from base.models import Season

from . import (
    SeasonSerializer,
    BasePlayerCardSerializer, PlayerCardSerializer,
    BaseClubSerializer, ClubLightListSerializer, BaseClubPlayerSerializer,
    CoachSerializer,
    LeagueSerializer,
    CountrySerializer,
    ClubListSerializer)
from ..models import Club, ClubPlayer, Coach, Player, League, Schedule


class ClubTeamPlayerSerializer(BasePlayerCardSerializer):
    url = serializers.ReadOnlyField(source='get_absolute_url')
    line_display = serializers.ReadOnlyField(source='get_line_display')
    birth_date_short = serializers.SerializerMethodField()
    citizenship = CountrySerializer()
    contract_to = serializers.SerializerMethodField()
    photo = serializers.ReadOnlyField(source='photo.url')
    is_joined = serializers.ReadOnlyField()
    is_left = serializers.ReadOnlyField()
    is_legionnaire = serializers.ReadOnlyField()
    is_home = serializers.ReadOnlyField()
    birth_place = serializers.ReadOnlyField()

    class Meta(object):
        fields = (
            'pk', 'url', 'number', 'line_display', 'name', 'lastname',
            'birth_date_short', 'citizenship', 'contract_to', 'photo',
            'is_joined', 'is_left', 'is_legionnaire', 'fio', 'is_home', 'birth_place')
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


class ClubTeamSerializer(BaseClubTeamSerializer):
    seasons = SeasonSerializer(many=True)
    address = AddressSerializer()
    league = LeagueSerializer()
    all_players = serializers.SerializerMethodField()  # for table view
    offender_players = serializers.SerializerMethodField()
    defender_players = serializers.SerializerMethodField()
    goalkeeper_players = serializers.SerializerMethodField()
    coaches = serializers.SerializerMethodField()

    _seasons_selected = None
    _players = None
    _coaches = None

    def _get_seasons(self, obj):
        ''' returns (prev, current, next) '''
        if self._seasons_selected is None:
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
        request = self.context.get('request')
        if self._players is not None:
            return self._players
        if request and request.GET.get('notplaying'):
            self._players = obj.get_not_playing_players()
            joined = left = frozenset()
        else:
            players = map(obj.get_players, self._get_seasons(obj))
            joined = set(players[1]) - set(players[0])  # joined club in current season
            left = set(players[1]) - set(players[2])  # left club in next season
            self._players = players[1]  # middle one is the current season
        for player in self._players:
            player.is_joined = player in joined
            player.is_left = player in left
            # воспитанник
            player.is_home = player.birth_place == obj.address.city
        return self._players

    def _get_coaches(self, obj):
        if self._coaches is None:
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

    def get_all_players(self, obj):
        players = sorted(list(self._get_players(obj)), key=lambda x: x.line)
        return ClubTeamPlayerSerializer(
            players, context=self.context, many=True).data

    def get_offender_players(self, obj):
        players = filter(lambda x: x.line == 3, self._get_players(obj))
        return ClubTeamPlayerSerializer(
            players, context=self.context, many=True).data

    def get_defender_players(self, obj):
        players = filter(lambda x: x.line == 2, self._get_players(obj))
        return ClubTeamPlayerSerializer(
            players, context=self.context, many=True).data

    def get_goalkeeper_players(self, obj):
        players = filter(lambda x: x.line == 1, self._get_players(obj))
        return ClubTeamPlayerSerializer(
            players, context=self.context, many=True).data

    def get_coaches(self, obj):
        coaches = self._get_coaches(obj)
        return ClubCoachSerializer(
            coaches, context=self.context, many=True).data

    def get_season(self, obj):
        return SeasonSerializer(
            self._get_seasons(obj)[1], context=self.context).data

    def get_prev_season(self, obj):
        return SeasonSerializer(
            self._get_seasons(obj)[0], context=self.context).data

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'site', 'contacts', 'coach', 'arena',
            'address', 'offender_players', 'all_players', 'league',
            'defender_players', 'goalkeeper_players', 'coaches',
            'url', 'seasons', 'season', 'prev_season')
        model = Club


class ClubPlayerSerializer(BaseClubPlayerSerializer):

    class Meta(object):
        fields = ('pk', 'player', 'club', )
        model = ClubPlayer


class LeagueClubsListSerializer(LeagueSerializer):
    clubs = ClubLightListSerializer(many=True)
    players_count = serializers.IntegerField()
    clubplayers = ClubPlayerSerializer(many=True)

    class Meta(object):
        fields = 'pk', 'title', 'clubs', 'players_count', 'clubplayers'
        model = League


class ClubTeamCompareSerializer(BaseClubTeamSerializer):
    source_season = serializers.SerializerMethodField()
    leagues = serializers.SerializerMethodField()

    _season = None
    _source_season = None
    _players = None
    _clubplayers = None

    def _get_season_from_params(self, obj, key):
        request = self.context.get('request')
        try:
            season = obj.seasons.get(
                pk=request.GET.get(key))
        except Season.DoesNotExist:
            season = obj.seasons[0]
        finally:
            return season

    def _get_season(self, obj):
        if self._season is None:
            self._season = self._get_season_from_params(
                obj, 'season')
        return self._season

    def _get_source_season(self, obj):
        if self._source_season is None:
            self._source_season = self._get_season_from_params(
                obj, 'source_season')
        return self._source_season

    def _get_players(self, obj):
        if self._players is None:
            season = self._get_source_season(obj)
            if season:
                clubplayer = obj.clubplayer_set.filter(season=season)
                players = Player.objects.filter(clubplayer__in=clubplayer)
                self._players = players
        return self._players

    def _get_leagues(self, obj):
        source_players = self._get_players(obj)
        season = self._get_season(obj)
        if season:
            same_club = (
                ClubPlayer.objects
                .filter(
                    player__in=source_players, season=season, club_id=obj.pk)
                .values_list('player_id', flat=True))
            clubplayers = (
                ClubPlayer.objects
                .filter(player__in=source_players, season=season)
                .exclude(player__in=same_club)
                .exclude(club_id=obj.pk)
                .order_by('club'))
            leagues = {}
            default_league = League(
                en_title=_('Other leagues'),
                ru_title=_('Other leagues'))
            for clubplayer in clubplayers:
                league = clubplayer.league or default_league
                leagues[league.pk] = league
                if not hasattr(league, 'clubs'):
                    league.clubs = []
                if not hasattr(league, 'players'):
                    league.players = []
                if not hasattr(league, 'clubplayers'):
                    league.clubplayers = []
                if not hasattr(league, 'clubplayers_count'):
                    league.clubplayers_count = 0
                if not hasattr(league, 'players_count'):
                    league.players_count = 0
                if clubplayer.club not in league.clubs:
                    league.clubs.append(clubplayer.club)
                if clubplayer.player not in league.players:
                    league.clubplayers.append(clubplayer)
                if clubplayer.player not in league.players:
                    league.players.append(clubplayer.player)
                    league.players_count += 1
            return leagues.values()

    def get_leagues(self, obj):
        return LeagueClubsListSerializer(
            self._get_leagues(obj), context=self.context, many=True).data

    def get_season(self, obj):
        season = self._get_season(obj)
        if season:
            return SeasonSerializer(season, context=self.context).data

    def get_prev_season(self, obj):
        seasons = list(obj.seasons)
        i = seasons.index(self._get_season(obj))
        season = None
        if i < len(seasons) - 1:
            season = seasons[i + 1]
        if season:
            return SeasonSerializer(season, context=self.context).data

    def get_source_season(self, obj):
        season = self._get_source_season(obj)
        if season:
            return SeasonSerializer(season, context=self.context).data

    class Meta(object):
        fields = (
            'pk', 'title', 'site', 'contacts', 'logo', 'url', 'source_season',
            'season', 'prev_season', 'leagues')
        model = Club


class ClubCalendarSerializer(serializers.ModelSerializer):
    home_team = ClubListSerializer()
    guest_team = ClubListSerializer()#BaseClubSerializer()
    is_home = serializers.SerializerMethodField()
    is_guest = serializers.SerializerMethodField()

    def get_is_home(self, obj):
        view = self.context['view']
        return int(view.kwargs.get('pk')) == obj.home_team.pk

    def get_is_guest(self, obj):
        view = self.context['view']
        return int(view.kwargs.get('pk')) == obj.guest_team.pk

    class Meta(object):
        fields = (
            'pk', 'date', 'home_team', 'guest_team', 'is_home', 'is_guest')
        model = Schedule


class ClubCalendarPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        season = get_object_or_404(
            Season, pk=self.request.GET.get('season', 0))
        return response.Response({
            'results': data,
            'season': SeasonSerializer(season).data,
        })


class NumbersClubPlayerSerializer(serializers.ModelSerializer):
    season = SeasonSerializer()

    class Meta(object):
        fields = 'pk', 'season', 'club_url'
        model = ClubPlayer


class NumbersPlayerSerializer(PlayerCardSerializer):
    clubplayers = NumbersClubPlayerSerializer(many=True)

    class Meta(PlayerCardSerializer.Meta):
        fields = PlayerCardSerializer.Meta.fields + ('clubplayers',)


class NumbersSerializer(serializers.ModelSerializer):
    players = NumbersPlayerSerializer(many=True)
    number = serializers.ReadOnlyField()

    class Meta(object):
        fields = 'players', 'number'
        model = Player
