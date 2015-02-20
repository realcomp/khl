# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from api.base.serializers import IIFMinimalSerializer
from hockeyapp.models import ClubPhotos, Club, Match


class ClubMinimalSerialiser(drf.serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = 'id', 'ru_title', 'get_absolute_url'
        read_only_fields = fields


class ClubPhotoSerializer(drf.serializers.ModelSerializer):
    photo = IIFMinimalSerializer()
    class Meta:
        model = ClubPhotos
        read_only_fields = 'photo',


class MatchMinimalSerialiser(drf.serializers.ModelSerializer):
    title = drf.serializers.ReadOnlyField(source='__unicode__')
    class Meta:
        model = Match
        fields = 'id', 'title'
        read_only_fields = fields