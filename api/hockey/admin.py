# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models import Q

import rest_framework as drf

from api.base.permissions import SportoAdminPermission
from api.base.paginators import AltPaginationSerializer
from hockeyapp.models import ClubPhotos, Club, Match, ArenaPhotos

from . import serializers


class CPAPIBase(object):
    queryset = ClubPhotos.objects.filter(processed=False)
    serializer_class = serializers.ClubPhotoSerializer
    permission_classes = (SportoAdminPermission,)
    pagination_serializer_class = AltPaginationSerializer
    paginate_by = 40


class ClubPhotosList(CPAPIBase, drf.generics.ListAPIView):
    b''' Список необработанных свежих фото из инстаграмма '''
cp_list = ClubPhotosList.as_view()


class ClubPhotosDetail(CPAPIBase, drf.generics.RetrieveUpdateDestroyAPIView):
    b''' Обновление данных фото из инстаграмма '''
cp_detail = ClubPhotosDetail.as_view()


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
        club = self.request.GET.get('club')
        q = Q()
        if club:
            q&= Q(home_team__pk=club) | Q(guest_team__pk=club)
        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            q&= Q(date__gte=date-datetime.timedelta(days=1)) & \
                Q(date__lte=date+datetime.timedelta(days=1))
        return qs.filter(q)
match_list = MatchList.as_view()


class ArenaPhotoList(drf.generics.ListCreateAPIView):
    queryset = ArenaPhotos.objects.all()
    serializer_class = serializers.ArenaPhotoSerializer
    permission_classes = (SportoAdminPermission,)
arenaphoto_list = ArenaPhotoList.as_view()