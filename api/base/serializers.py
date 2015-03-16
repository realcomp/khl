# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from filer.models import Image

from base.models import InstagramImageFile, InstagramUser


class LangDepSerializer(drf.serializers.ModelSerializer):
    '''
    Language-Dependent Serializer
    '''
    def _get_field(self, obj, field_name):
        return obj.get_locale_attr(
            field_name, request=self.context.get('request'))


class TitleBaseSerializer(LangDepSerializer):
    title = drf.serializers.SerializerMethodField()
    get_title = lambda self, obj: self._get_field(obj, 'title')


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