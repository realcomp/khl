# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, TemplateView

from ...models import Player
from ...serializers import PlayerCardSerializer


class Index(TemplateView):
    def get_template_names(self):
        version = 'CLASSIC'
        if self.request.user.is_authenticated():

            # TODO: remove it when index template will be competed
            if self.request.user.version == 'PRO':
                return ['hockeyapp/v1/metrics/player-select.html']

            version = self.request.user.version
        return ['hockeyapp/v1/index-%s.html' % version.lower()]
index = Index.as_view()


class IndexClassic(TemplateView):
    version = 'CLASSIC'

    def get_template_names(self):
        return ['hockeyapp/v1/index-%s.html' % self.version.lower()]

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            if self.request.user.version != self.version:
                self.request.user.version = self.version
                self.request.user.save(update_fields=['version'])
        return super(IndexClassic, self).get(
            self, request, *args, **kwargs)


class IndexPro(IndexClassic):
    version = 'PRO'

    # TODO: remove it when index template will be competed
    def get_template_names(self):
        return ['hockeyapp/v1/metrics/player-select.html']


class MetricsPlayers(TemplateView):
    template_name = 'hockeyapp/v1/metrics/player-select.html'


class MetricsPlayerCard(DetailView):
    model = Player
    template_name = 'hockeyapp/v1/metrics/player-card.html'

    def get_context_data(self, **kwargs):
        context = super(MetricsPlayerCard, self).get_context_data(**kwargs)
        context['request'] = self.request
        context.update(PlayerCardSerializer(
            self.get_object(), context=context).data)
        return context


class MetricsPlayersCompare(TemplateView):
    template_name = 'hockeyapp/v1/metrics/players-diff.html'


class MetricsPlayersCompareGraph(TemplateView):
    template_name = 'hockeyapp/v1/metrics/players-diff3.html'
