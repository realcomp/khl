# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from api.base.permissions import SportoAdminPermission
from hockeyapp.models import ClubPhotos

from . import serializers


class CPAPIBase(object):
    queryset = ClubPhotos.objects.filter(processed=False)
    serializer_class = serializers.ClubPhotoSerializer
    permission_classes = (SportoAdminPermission,)
    paginate_by = 500


class ClubPhotosList(CPAPIBase, drf.generics.ListAPIView):
    b''' Список необработанных свежих фото из инстаграмма '''
cp_list = ClubPhotosList.as_view()


class ClubPhotosDetail(CPAPIBase, drf.generics.RetrieveUpdateDestroyAPIView):
    b''' Обновление данных фото из инстаграмма '''
cp_detail = ClubPhotosDetail.as_view()