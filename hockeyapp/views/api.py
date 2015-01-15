# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools
import json
import operator

from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import generics

from addresses.models import Country

from .mixins import PaginationMixin
from ..serializers import (
    PlayerCardSerializer, ClubListSerializer, MetricsPlayerSerializer,
    CountryLeaguesSerializer)
from ..models import Club, Player, ClubPlayer


class PlayersSearch(PaginationMixin, generics.ListAPIView):
    # permission_classes = permissions.IsAuthenticated,
    serializer_class = PlayerCardSerializer

    def get_queryset(self):
        return Player.objects.all()

    def filter_queryset(self, qs):
        qs = super(PlayersSearch, self).filter_queryset(qs)
        club = None
        citizenship = []
        if 'line' in self.request.GET:
            # union of sets
            values = reduce(operator.or_, map(set, map(
                json.loads, self.request.GET.getlist('line'))))
            qs = qs.filter(line__in=values)
        if 'citizenship' in self.request.GET:
            citizenship += filter(
                None, self.request.GET.getlist('citizenship'))
        if ('citizenship_other' in self.request.GET and
                'citizenship_other_active' in self.request.GET):
            citizenship += filter(
                None, self.request.GET.getlist('citizenship_other'))
        if citizenship:
            qs = qs.filter(citizenship__in=citizenship)
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
        if 'order_by' in self.request.GET:
            field = self.request.GET['order_by']
            if '%s' in field:
                field = field % self.request.LANGUAGE_CODE
            qs = qs.order_by(field)
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


class LeagueList(generics.ListAPIView):
    serializer_class = CountryLeaguesSerializer

    def get_queryset(self):
        return Country.objects.exclude(league__isnull=True)


class ClubList(PaginationMixin, generics.ListAPIView):
    # permission_classes = permissions.IsAuthenticated,
    serializer_class = ClubListSerializer

    def get_queryset(self):
        return Club.objects.all()

    def filter_queryset(self, qs):
        qs = super(ClubList, self).filter_queryset(qs)
        if 'order_by' in self.request.GET:
            field = self.request.GET['order_by']
            if '%s' in field:
                field = field % self.request.LANGUAGE_CODE
            qs = qs.order_by(field)
        country = Country.objects.filter(ru_title=b'Россия').last()
        if 'country' in self.request.GET:
            country = get_object_or_404(
                Country, pk=self.request.GET['country'])
        if country:
            qs = qs.filter(leagueclub__league__country_id=country)
        if 'league' in self.request.GET:
            league = self.request.GET['league']
            if league:
                qs = qs.filter(leagueclub__league_id=league)
        return qs


class MetricsPlayers(generics.ListAPIView):
    paginate_by = 100
    # permission_classes = permissions.IsAuthenticated,
    serializer_class = MetricsPlayerSerializer

    def get_queryset(self):
        return Player.objects.all()
