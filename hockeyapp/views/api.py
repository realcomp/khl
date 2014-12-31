# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import operator

from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions

from ..serializers import PlayerCardSerializer, ClubListSerializer
from ..models import Club, Player


class PlayersSearch(generics.ListAPIView):
    paginate_by = 100
    permission_classes = permissions.IsAuthenticated,
    serializer_class = PlayerCardSerializer

    def get_queryset(self):
        return Player.objects.all()

    def filter_queryset(self, qs):
        qs = super(PlayersSearch, self).filter_queryset(qs)
        club = None
        if 'line' in self.request.GET:
            # union of sets
            values = reduce(operator.or_, map(set, map(
                json.loads, self.request.GET.getlist('line'))))
            qs = qs.filter(line__in=values)
        if 'club' in self.request.GET:
            club = get_object_or_404(Club, pk=self.request.GET['club'])
        if 'season' in self.request.GET and club:
            season = json.loads(self.request.GET['season'])
            qs = qs.by_season(club, season)
        return qs


class ClubList(generics.ListAPIView):
    paginate_by = 100
    permission_classes = permissions.IsAuthenticated,
    serializer_class = ClubListSerializer

    def get_queryset(self):
        return Club.objects.all()

    def filter_queryset(self, qs):
        qs = super(ClubList, self).filter_queryset(qs)
        if 'order_by' in self.request.GET:
            qs = qs.order_by(
                self.request.GET['order_by'] % self.request.LANGUAGE_CODE)
        return qs
