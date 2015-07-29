# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import itertools

from rest_framework import generics, response, viewsets

from ...search import SearchResultFactory
from ...models import Club, Player, ClubPlayerMatch, Schedule, ClubPlayer
from ...models import Timeline
from ...serializers.search import SearchResultSerializer


class Search(generics.ListAPIView):
    serializer_class = SearchResultSerializer

    def get_queryset(self):
        factory = SearchResultFactory(sources={
            'club': Club.objects,
            'player': Player.objects,
            'schedule': Schedule.objects,
        })
        return factory.get_results(self.request.QUERY_PARAMS.get('s'))
