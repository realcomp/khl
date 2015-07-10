# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import Season


class LangDepSerializer(serializers.ModelSerializer):
    '''
    Language-Dependent Serializer
    '''
    def _get_field(self, obj, field_name):
        return obj.get_locale_attr(
            field_name, request=self.context.get('request'))


class TitleBaseSerializer(LangDepSerializer):
    title = serializers.SerializerMethodField()
    get_title = lambda self, obj: self._get_field(obj, 'title')


class SeasonsMenuItemSerializer(TitleBaseSerializer):
    '''
    Basic serializer for seasons dropdown menu
    '''
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        ''' 2015-16 '''
        return '%d-%s' % (obj.start_date.year, str(obj.end_date.year)[2:])

    class Meta(object):
        fields = 'pk', 'label'
        model = Season
