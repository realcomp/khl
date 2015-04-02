# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models import Q

import rest_framework as drf

from api.base.permissions import SportoAdminPermission
from api.base.paginators import AltPaginationSerializer
from hockeyapp.models import ArenaInstaPhoto, Club, Match, Player, Arena

from . import serializers


class CPAPIBase(object):
    queryset = ArenaInstaPhoto.objects.all()
    serializer_class = serializers.ArenaInstaPhotoSerializer
    permission_classes = (SportoAdminPermission,)
    pagination_serializer_class = AltPaginationSerializer
    paginate_by = 40


class ArenaInstaPhotoList(CPAPIBase, drf.generics.ListAPIView):
    b''' Список необработанных свежих фото из инстаграмма '''
    def filter_queryset(self, qs):
        qs = super(ArenaInstaPhotoList, self).filter_queryset(qs)
        processed = self.request.GET.get('processed')
        if processed:
            qs = qs.to_view()
        else:
            qs = qs.for_moderation()
        max_id = self.request.GET.get('max_id')
        min_id = self.request.GET.get('min_id')
        club = self.request.GET.get('club')
        if club:
            qs = qs.club_photo(club)
        q = Q()
        if max_id:
            q&= Q(id__lt=max_id)
        if min_id:
            q&= Q(id__gte=min_id)
        return qs.filter(q)
aip_list = ArenaInstaPhotoList.as_view()


class ArenaInstaPhotoDetail(CPAPIBase, drf.generics.RetrieveUpdateDestroyAPIView):
    b''' Обновление данных фото из инстаграмма '''
aip_detail = ArenaInstaPhotoDetail.as_view()


class ArenaList(drf.generics.ListAPIView):
    queryset = Arena.objects.all()
    serializer_class = serializers.ArenaMinimalSerialiser
    permission_classes = (SportoAdminPermission,)
arena_list = ArenaList.as_view()


class ArenaDetail(drf.generics.RetrieveAPIView):
    queryset = Arena.objects.all()
    serializer_class = serializers.ArenaMinimalSerialiser
    permission_classes = (SportoAdminPermission,)
arena_detail = ArenaDetail.as_view()


class ClubList(drf.generics.ListAPIView):
    queryset = Club.objects.all()
    serializer_class = serializers.ClubMinimalSerialiser
    permission_classes = (SportoAdminPermission,)
club_list = ClubList.as_view()


class ClubDetail(drf.generics.RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = serializers.ClubMinimalSerialiser
    permission_classes = (SportoAdminPermission,)
club_detail = ClubDetail.as_view()


class MatchList(drf.generics.ListAPIView):
    queryset = Match.objects.all()
    serializer_class = serializers.MatchMinimalSerialiser
    permission_classes = (SportoAdminPermission,)

    def filter_queryset(self, qs):
        qs = super(MatchList, self).filter_queryset(qs)
        date = self.request.GET.get('date')
        arena = self.request.GET.get('arena')
        q = Q()
        if arena:
            q&= Q(home_team__arena_id=arena)
        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            q&= Q(date__gte=date-datetime.timedelta(days=1)) & \
                Q(date__lte=date+datetime.timedelta(days=1))
        return qs.filter(q)
match_list = MatchList.as_view()


class PlayerList(drf.generics.ListAPIView):
    queryset = Player.objects.filter(number__isnull=False).exclude(number='')
    serializer_class = serializers.PlayerMinimalSerialiser
    permission_classes = (SportoAdminPermission,)

    def filter_queryset(self, qs):
        qs = super(PlayerList, self).filter_queryset(qs)
        club = self.request.GET.getlist('club')
        q = Q()
        if club:
            q&= Q(club__in=set(club))
            number = self.request.GET.getlist('number')
            if number:
                q&= Q(number__in=set(number))
            return qs.filter(q)
        else:
            return qs.none()
player_list = PlayerList.as_view()