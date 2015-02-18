# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from api.base.permissions import SportoAdminPermission
from api.base.paginators import AltPaginationSerializer
from hockeyapp.models import ClubPhotos

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