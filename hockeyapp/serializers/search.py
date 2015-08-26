# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..search import ClubSearchResult, PlayerSearchResult


class SearchResultSerializer(serializers.Serializer):
    title = serializers.SerializerMethodField()

    def get_title(self, event):
        request = self.context.get('request')
        if isinstance(event, ClubSearchResult):
            return event.obj.get_locale_attr('title', request=request)
        elif isinstance(event, PlayerSearchResult):
            name = event.obj.get_locale_attr('name', request=request)
            lastname = event.obj.get_locale_attr('lastname', request=request)
            return '%s %s' % (lastname, name)

    class Meta(object):
        fields = 'title',
