# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from base.models import Season

from ..serializers import SeasonSerializer


class SeasonsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(SeasonsMixin, self).get_context_data(**kwargs)
        context['request'] = self.request
        seasons = self.get_object().seasons
        context['seasons'] = SeasonSerializer(
            seasons, context=context, many=True).data
        if 'season' in self.request.GET:
            default_season = get_object_or_404(
                Season, pk=self.request.GET['season'])
        else:
            default_season = seasons[0] if seasons else None
        context['default_season'] = SeasonSerializer(
            default_season, context=context).data
        return context
