# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

from ..models import Club, Player, Schedule
from ..search import SearchResultFactory
from ..serializers.search import SearchResultSerializer


class Search(TemplateView):
    template_name = 'hockeyapp/search.html'

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['request'] = self.request
        query = self.request.GET.get('s')
        if query:
            context['query'] = query
            factory = SearchResultFactory(sources={
                'club': Club.objects,
                'player': Player.objects,
                'schedule': Schedule.objects,
            })
            results = factory.get_results(query)
            context['results'] = SearchResultSerializer(
                results, context=context, many=True).data
        return context
