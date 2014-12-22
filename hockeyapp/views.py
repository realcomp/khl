# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, TemplateView

from .serializers import PlayerCardSerializer
from .models import Player


class PlayersSearch(ListView):
    model = Player
    paginate_by = 100
    template_name = 'hockeyapp/players-search.html'

    def get_context_data(self, **kwargs):
        context = super(PlayersSearch, self).get_context_data(**kwargs)
        qs = self.get_queryset()
        page_size = self.get_paginate_by(qs)
        paginator, page, object_list, has_other_pages = self.paginate_queryset(
            qs, page_size)
        context.update({
            'count': qs.count(),
            'results': PlayerCardSerializer(object_list, many=True).data,
        })
        return context


class PlayersCompare(TemplateView):
    template_name = 'hockeyapp/player-select.html'
    # related templates:
    # players-diff.html
    # players-diff2.html
    # players-diff3.html
    # player-card.html


class PlayerCard(DetailView):
    model = Player
    template_name = 'hockeyapp/player-card-short.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerCard, self).get_context_data(**kwargs)
        context.update(PlayerCardSerializer(self.get_object()).data)
        return context


class PlayerCardIndicators(PlayerCard):
    template_name = 'hockeyapp/player-card-indicators.html'


class PlayerCardClubs(PlayerCard):
    template_name = 'hockeyapp/player-card-clubs.html'


class PlayerCardCoaches(PlayerCard):
    template_name = 'hockeyapp/player-card-coaches.html'


class PlayerCardPartners(PlayerCard):
    template_name = 'hockeyapp/player-card-partners.html'


class PlayerCardPhotos(PlayerCard):
    template_name = 'hockeyapp/player-card-photos.html'


class PlayerCardCommunication(PlayerCard):
    template_name = 'hockeyapp/player-card-communication.html'


class PlayerCardNews(PlayerCard):
    template_name = 'hockeyapp/player-card-news.html'
