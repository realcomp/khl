# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from api.base.serializers import IIFMinimalSerializer
from hockeyapp.models import ClubPhotos, Club


class ClubMinimalSerialiser(drf.serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = 'id', 'ru_title'
        read_only_fields = fields


class ClubPhotoSerializer(drf.serializers.ModelSerializer):
    club = ClubMinimalSerialiser()
    photo = IIFMinimalSerializer()
    class Meta:
        model = ClubPhotos
        read_only_fields = 'photo', 'club'