# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools
import json
import operator

from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import generics

from ..serializers import (
    PlayerCardSerializer, ClubListSerializer, MetricsPlayerSerializer)
from ..models import Club, Player, ClubPlayer


class PlayersSearch(generics.ListAPIView):
    # permission_classes = permissions.IsAuthenticated,
    serializer_class = PlayerCardSerializer

    def get_queryset(self):
        return Player.objects.all()

    def get_paginate_by(self):
        if 'paginate_by' in self.request.GET:
            return int(self.request.GET['paginate_by'])
        return 50

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
        if 'order_by' in self.request.GET:
            field = self.request.GET['order_by']
            if '%s' in field:
                field = field % self.request.LANGUAGE_CODE
            qs = qs.order_by(field)
        # get clubs
        club_players = (
            ClubPlayer.objects
            .filter(player__in=qs)
            .order_by('-end_date')
            .values_list('player_id', 'club_id'))
        club_players2 = qs.values_list('id', 'club')
        clubs = {
            club.pk: club
            for club in Club.objects
            .filter(
                Q(pk__in=zip(*club_players)[1]) |
                Q(pk__in=zip(*club_players2)[1]))}
        self.players_clubs = {}
        for player_id, club_id in filter(
                lambda x: x[1], itertools.chain(club_players2, club_players)):
            if player_id not in self.players_clubs:
                self.players_clubs[player_id] = []
            if clubs[club_id] not in self.players_clubs[player_id]:
                self.players_clubs[player_id].append(clubs[club_id])
        return qs


class ClubList(generics.ListAPIView):
    paginate_by = 100
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
        return qs


class MetricsPlayers(generics.ListAPIView):
    paginate_by = 100
    # permission_classes = permissions.IsAuthenticated,
    serializer_class = MetricsPlayerSerializer

    def get_queryset(self):
        return Player.objects.all()
