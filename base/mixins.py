# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from .models import Season
from .serializers import SeasonsMenuItemSerializer


class SeasonsMenuMixin(object):
    '''
    Adds seasons menu data into context
    '''
    def get_context_data(self, **kwargs):
        context = super(SeasonsMenuMixin, self).get_context_data(**kwargs)
        context['request'] = self.request

        seasons = self.get_object().seasons
        context['seasons'] = SeasonsMenuItemSerializer(
            seasons, context=context, many=True).data

        _season = self.request.GET.get('season')
        if _season:
            default_season = get_object_or_404(Season, pk=_season)
        else:
            default_season = seasons[0] if seasons else None

        context['default_season'] = SeasonsMenuItemSerializer(
            default_season, context=context).data
        return context
