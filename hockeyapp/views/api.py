# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import itertools
import json
import operator

from django.db.models import Avg, Q, Max, Min, Sum
from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets

from addresses.models import Country
from base.models import Season

from .mixins import PaginationMixin, OrderMixin
from ..models import Club, Player, ClubPlayer, ClubPlayerMatch
from ..serializers import (
    CountryLeaguesSerializer,
    PlayerCardSerializer,
    ClubListSerializer,
    MetricsPlayerSerializer,
)
from ..serializers.clubs import ClubTeamSerializer, ClubTeamCompareSerializer
from ..serializers.players import ClubPlayerMatchSerilizer
from ..utils import month_range


class PlayersSearch(
        PaginationMixin, OrderMixin, viewsets.ReadOnlyModelViewSet):
    # permission_classes = permissions.IsAuthenticated,
    serializer_class = PlayerCardSerializer

    def get_queryset(self):
        return Player.objects.all()

    def filter_queryset(self, qs):
        qs = super(PlayersSearch, self).filter_queryset(qs)

        if 'line' in self.request.GET:
            # union of sets
            values = reduce(operator.or_, map(set, map(
                json.loads, self.request.GET.getlist('line'))))
            qs = qs.filter(line__in=values)

        q_citizenship = None
        if 'citizenship' in self.request.GET:
            citizenship = filter(None, self.request.GET.getlist('citizenship'))
            if citizenship:
                q = Q(citizenship__in=citizenship)
                q_citizenship = (q_citizenship | q) if q_citizenship else q
        if ('citizenship_other' in self.request.GET and
                'citizenship_other_active' in self.request.GET):
            citizenship_other = filter(
                None, self.request.GET.getlist('citizenship_other'))
            if citizenship_other:
                q = Q(citizenship__in=citizenship_other)
            else:
                q = ~Q(citizenship__ru_title=b'Россия')
            q_citizenship = (q_citizenship | q) if q_citizenship else q
        if q_citizenship:
            qs = qs.filter(q_citizenship)

        club = None
        if 'club' in self.request.GET:
            club = get_object_or_404(Club, pk=self.request.GET['club'])

        if 'season' in self.request.GET and club:
            season = json.loads(self.request.GET['season'])
            qs = qs.by_season(club, season)

        if 'league' in self.request.GET:
            leagues = self.request.GET.getlist('league')
            # qs = (
            #     qs.filter(
            #         Q(club__leagueclub__league_id__in=leagues) |
            #         Q(clubplayer__club__leagueclub__league_id__in=leagues))
            #     .distinct())
            qs = qs.filter(club__leagueclub__league_id__in=leagues)

        # get clubs
        club_players = qs.values_list('id', 'club')
        club_players2 = (
            ClubPlayer.objects
            .filter(player__in=qs)
            .order_by('-end_date')
            .values_list('player_id', 'club_id'))
        clubs_q = Q()
        if club_players:
            clubs_q |= Q(pk__in=zip(*club_players)[1])
        if club_players2:
            clubs_q |= Q(pk__in=zip(*club_players2)[1])
        clubs = {
            club.pk: club for club in Club.objects.filter(clubs_q)}
        self.players_clubs = {}
        for player_id, club_id in filter(
                lambda x: x[1], itertools.chain(club_players, club_players2)):
            if player_id not in self.players_clubs:
                self.players_clubs[player_id] = []
            if clubs[club_id] not in self.players_clubs[player_id]:
                self.players_clubs[player_id].append(clubs[club_id])
        return qs


class PlayerCardIndicators(generics.ListAPIView):
    paginate_by = 99999
    serializer_class = ClubPlayerMatchSerilizer

    def _get_aggregate(self, qs):
        return qs.aggregate(*itertools.chain(
            map(Sum, (
                'plus_minus', 'penalty_time', 'ev_goals', 'pp_goals',
                'es_goals', 'overtime_goals', 'win_goals', 'bullet_goals',
                'shots', 'faceoff', 'winfaceoff', 'winfaceoff_p')),
            map(Avg, (
                'shots', 'pis', 'winfaceoff_p', 'gamingtime',
                'change_count')),
        ))

    def get_queryset(self):
        return ClubPlayerMatch.objects.all()

    def filter_queryset(self, qs):
        qs = super(PlayerCardIndicators, self).filter_queryset(qs)

        clubplayers = (
            ClubPlayer.objects
            .filter(player_id=self.kwargs.get('player_id', 0)))

        if 'season' in self.request.GET:
            clubplayers = clubplayers.filter(
                season_id=self.request.GET['season'])

        if 'club' in self.request.GET:
            clubplayers = clubplayers.filter(club_id=self.request.GET['club'])

        if 'coach' in self.request.GET:
            clubplayers = clubplayers.filter(
                club__coachclub__coach_id=self.request.GET['coach'],
                season__coachclub__coach_id=self.request.GET['coach'])

        qs = qs.filter(clubplayer__in=clubplayers)

        if self.request.GET.get('group_by') == 'season':
            seasons = (
                Season.objects
                .filter(pk__in=clubplayers.values_list('season_id'))
                .order_by('start_date'))
            qss = []
            for season in seasons:
                season_qs = qs.filter(clubplayer__season=season)
                season_qs.date = None
                season_qs.season = season
                season_qs._aggregate = self._get_aggregate(season_qs)
                qss.append(season_qs)
            return qss
        else:  # group by month (by default)
            min_max = qs.aggregate(Min('match__date'), Max('match__date'))
            start_date = min_max.get('match__date__min')
            end_date = min_max.get('match__date__max')
            if start_date and end_date:
                qss = []
                dates = list(month_range(start_date, end_date))
                for i in range(len(dates) - 1):
                    month_qs = qs.filter(
                        match__date__gt=dates[i],
                        match__date__lte=dates[i + 1])
                    month_qs.date = dates[i]
                    month_qs.season = None
                    month_qs._aggregate = self._get_aggregate(month_qs)
                    qss.append(month_qs)
                return qss
        return []


class LeagueList(generics.ListAPIView):
    serializer_class = CountryLeaguesSerializer

    def get_queryset(self):
        return Country.objects.exclude(league__isnull=True)


class ClubList(PaginationMixin, OrderMixin, generics.ListAPIView):
    # permission_classes = permissions.IsAuthenticated,
    serializer_class = ClubListSerializer

    def get_queryset(self):
        return Club.objects.all()

    def filter_queryset(self, qs):
        qs = super(ClubList, self).filter_queryset(qs)

        country = Country.objects.filter(ru_title=b'Россия').last()
        if 'country' in self.request.GET:
            country = get_object_or_404(
                Country, pk=self.request.GET['country'])
        if country:
            qs = qs.filter(leagueclub__league__country_id=country).distinct()

        if 'league' in self.request.GET:
            league = self.request.GET['league']
            if league:
                qs = qs.filter(leagueclub__league_id=league).distinct()

        if 'season' in self.request.GET:
            season = self.request.GET['season']
            if season:
                qs = qs.by_season(json.loads(season)).distinct()

        return qs


class ClubTeam(generics.RetrieveAPIView):
    serializer_class = ClubTeamSerializer

    def get_queryset(self):
        return Club.objects.all()


class ClubTeamCompare(generics.RetrieveAPIView):
    serializer_class = ClubTeamCompareSerializer

    def get_queryset(self):
        return Club.objects.all()


class MetricsPlayers(generics.ListAPIView):
    paginate_by = 100
    # permission_classes = permissions.IsAuthenticated,
    serializer_class = MetricsPlayerSerializer

    def get_queryset(self):
        return Player.objects.all()
