# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..search import PlayerSearchResult


class SearchResultSerializer(serializers.Serializer):
    title = serializers.SerializerMethodField()

    def get_title(self, event):
        request = self.context.get('request')
        if isinstance(event, PlayerSearchResult):
            name = event.obj.get_locale_attr('name', request=request)
            lastname = event.obj.get_locale_attr('lastname', request=request)
            return '%s %s' % (lastname, name)

    class Meta(object):
        fields = 'title',
