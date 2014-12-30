# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import operator

from rest_framework import generics, permissions

from ..serializers import PlayerCardSerializer
from ..models import Club, Player


class PlayersSearch(generics.ListAPIView):
    paginate_by = 100
    permission_classes = permissions.IsAuthenticated,
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
        return qs
