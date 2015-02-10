# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools
import json
import operator

from django.db.models import Avg, Sum, Count
from django.shortcuts import get_object_or_404

from rest_framework import generics, response, viewsets

from addresses.models import Country

from base.models import Season

from .mixins import PaginationMixin
from ..filters import (
    PlayersSearchFilter, OrderFilter, PlayersSearchOrderFilter)
from ..models import Club, Player, ClubPlayer, ClubPlayerMatch, LeagueClub
from ..serializers import (
    CountryLeaguesSerializer,
    ClubListSerializer,
    MetricsPlayerSerializer,
)
from ..serializers.clubs import ClubTeamSerializer, ClubTeamCompareSerializer
from ..serializers.players import (
    PlayersSearchSerializer, ClubPlayerMatchSerilizer)


class PlayersSearch(
        PaginationMixin, viewsets.ReadOnlyModelViewSet):
    filter_backends = PlayersSearchFilter, PlayersSearchOrderFilter
    queryset = Player.objects.all()
    serializer_class = PlayersSearchSerializer

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())

        # get clubplayers
        self.clubplayers = {}
        clubplayers = (
            ClubPlayer.objects
            .filter(pk__in=qs.values_list('clubplayer', flat=True))
            .order_by('-end_date'))
        for clubplayer in clubplayers:
            player_id = clubplayer.player_id
            if player_id not in self.clubplayers:
                self.clubplayers[player_id] = []
            if clubplayer not in self.clubplayers[player_id]:
                self.clubplayers[player_id].append(clubplayer)

        # get rating
        rated_qs = qs
        rated_by = self.request.GET.get('rated_by', 'seasons_total')
        if rated_by:
            rated_qs = qs.order_by('-' + rated_by)
        self.rating = {}
        rating_index = 0
        rating_value = None
        for player in rated_qs:
            if rated_by:
                if (getattr(player, rated_by) < rating_value or
                        rating_value is None):
                    rating_index += 1
                    rating_value = getattr(player, rated_by)
            else:
                rating_index += 1
            self.rating[player.pk] = rating_index

        return super(PlayersSearch, self).list(request, *args, **kwargs)


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
            return qs.group_by_season()
        else:  # group by month (by default)
            return qs.group_by_month()


class LeagueList(generics.ListAPIView):
    serializer_class = CountryLeaguesSerializer

    def get_queryset(self):
        return Country.objects.exclude(league__isnull=True)


class ClubList(PaginationMixin, generics.ListAPIView):
    filter_backends = OrderFilter,
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
