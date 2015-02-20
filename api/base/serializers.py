# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from filer.models import Image

from base.models import InstagramImageFile


class FIFSerialiser(drf.serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = 'id', 'file', 'name', '_height', '_width'
        read_only_fields = fields


class IIFMinimalSerializer(drf.serializers.ModelSerializer):
    img = FIFSerialiser()
    class Meta:
        model = InstagramImageFile
        fields = 'id', 'img', 'created'