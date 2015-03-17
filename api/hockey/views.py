# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from django.db.models import Q

from hockeyapp.filters import OrderFilter
from hockeyapp.views.mixins import PaginationMixin
from hockeyapp.models import Club, Country

from .admin import ArenaInstaPhotoList
from .serializers import ClubListSerializer


class ClubInstaPhotoList(ArenaInstaPhotoList):
    b''' прошедшие модерацию инстаграмм фото клуба '''
    permission_classes = ()
    def filter_queryset(self, qs):
        processed = self.request.GET.get('processed')
        if processed:
            return super(ClubInstaPhotoList, self).filter_queryset(qs)
        else:
            return qs.none()
cip_list = ClubInstaPhotoList.as_view()


class PlayerInstaPhotoList(ClubInstaPhotoList):
    b''' прошедшие модерацию инстаграмм фото игрока '''
    def filter_queryset(self, qs):
        qs = super(PlayerInstaPhotoList, self).filter_queryset(qs)
        if self.request.GET.get('player'):
            qs = qs.player_photo(self.request.GET.get('player'))
        return qs
pip_list = PlayerInstaPhotoList.as_view()


class ProcessedArenaInstaPhotoList(ClubInstaPhotoList):
    b''' прошедшие модерацию инстаграмм фото арены '''
    def filter_queryset(self, qs):
        qs = super(ProcessedArenaInstaPhotoList, self).filter_queryset(qs)
        if self.request.GET.get('arena'):
            qs = qs.arena_photo(self.request.GET.get('arena'))
        return qs
paip_list = ProcessedArenaInstaPhotoList.as_view()


class ClubList(PaginationMixin, drf.generics.ListAPIView):
    filter_backends = OrderFilter,
    serializer_class = ClubListSerializer

    def get_queryset(self):
        return Club.objects.all()

    def filter_queryset(self, qs):
        qs = super(ClubList, self).filter_queryset(qs)
        q = Q()
        if 'country' in self.request.GET:
            country = Country.objects.filter(pk=self.request.GET['country']
                                    ).last()
        else:
            country = Country.objects.filter(ru_title=b'Россия'
                                    ).last()
        if country:
            q&= Q(leagueclub__league__country_id=country)
        if self.request.GET.get('league'):
            league = self.request.GET['league']
            q&= Q(leagueclub__league_id=league)
        ids = set(qs.filter(q).values_list('pk', flat=True))
        qs = qs.filter(pk__in=ids)
        return qs
club_list = ClubList.as_view()