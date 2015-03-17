# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from base.models import InstagramUser

from .permissions import SportoAdminPermission

from . import serializers


class IUAPIBase(object):
    queryset = InstagramUser.objects.all()
    serializer_class = serializers.InstagramUserSerializer
    permission_classes = (SportoAdminPermission,)

class InstagramUserList(IUAPIBase, drf.generics.ListAPIView):
    b''' список инстаграм пользователей'''
iu_list = InstagramUserList.as_view()


class InstagramUserDetail(IUAPIBase, drf.generics.RetrieveAPIView):
    b''' инстаграм пользователь'''
iu_detail = InstagramUserDetail.as_view()