# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import operator

from django.shortcuts import get_object_or_404

from rest_framework import generics

from ..serializers import (
    PlayerCardSerializer, ClubListSerializer, MetricsPlayerSerializer)
from ..models import Club, Player


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
