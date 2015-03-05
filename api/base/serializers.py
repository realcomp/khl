# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from filer.models import Image

from base.models import InstagramImageFile, InstagramUser


class FIFSerialiser(drf.serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = 'id', 'file', 'name', '_height', '_width'
        read_only_fields = fields


class InstagramUserSerializer(drf.serializers.ModelSerializer):
    class Meta:
        model = InstagramUser


class IIFMinimalSerializer(drf.serializers.ModelSerializer):
    img = FIFSerialiser()
    #instagram_user = InstagramUserSerializer()
    class Meta:
        model = InstagramImageFile
        fields = 'id', 'img', 'created', 'instagram_user', 'comment'