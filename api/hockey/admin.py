# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models import Q
from django.db.models.loading import get_model

import rest_framework as drf
import filer

from api.base.permissions import SportoAdminPermission
from api.base.paginators import AltPagination
from hockeyapp.models import ArenaInstaPhoto, Club, Match, Player, Arena

from . import serializers


class FilerImageUpload(drf.views.APIView):
    permission_classes = (SportoAdminPermission,)
    allowed_methods = ('POST', 'PUT')

    def post(self, request, format=None):
        print request
        print request.data
        if request.data:
            fl = request.data.get('file')
            model_name = request.data.get('model_name','').capitalize()
            model = get_model('hockeyapp', model_name)
            instance_id = request.data.get('id')
            filer_file = self.create_filer_image(fl, model_name)
            if self.set_relation(filer_file, model, instance_id):
                return drf.response.Response(status=201)
        return drf.response.Response(status=404)

    def put(self, request, format=None):
        return self.post(request, format)

    def create_filer_image(self, image, folder_name):
        _folder_objects = filer.models.Folder.objects
        folder = _folder_objects.filter(name=folder_name).last()
        if not folder:
            folder = _folder_objects.create(name=folder_name)
        _file_objects = filer.models.Image.objects
        data = dict(folder=folder,
                    name=image.name,
                    is_public=True
        )
        _file = _file_objects.filter(**data).last()
        if not _file:
            _file = _file_objects.create(**data)
            _file.file.save(image.name, image)
            _file.save()
        return _file

    def set_relation(self, filer_image, model, instance_id):
        instance = model.objects.filter(pk=instance_id).last()
        if instance:
            instance.photo = filer_image
            instance.save(update_fields=['photo'])
            return 1
fiu_admin = FilerImageUpload.as_view()

class CPAPIBase(object):
    queryset = ArenaInstaPhoto.objects.all()
    serializer_class = serializers.ArenaInstaPhotoSerializer
    permission_classes = (SportoAdminPermission,)
    pagination_class = AltPagination
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
    queryset = Club.objects.active()
    serializer_class = serializers.ClubMinimalSerialiser
    permission_classes = (SportoAdminPermission,)
club_list = ClubList.as_view()


class ClubDetail(drf.generics.RetrieveAPIView):
    queryset = Club.objects.active()
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
