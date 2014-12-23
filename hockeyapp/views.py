# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, TemplateView

from .serializers import (
    ClubListSerializer, ClubSerializer, PlayerCardSerializer)
from .models import Club, Player


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


class PlayersCompareCard(TemplateView):
    template_name = 'hockeyapp/player-card.html'


class PlayersCompareDiff(TemplateView):
    template_name = 'hockeyapp/players-diff.html'


class PlayersCompareDiff2(TemplateView):
    template_name = 'hockeyapp/players-diff2.html'


class PlayersCompareDiff3(TemplateView):
    template_name = 'hockeyapp/players-diff3.html'


class PlayerCard(DetailView):
    model = Player
    template_name = 'hockeyapp/players/player-card-short.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerCard, self).get_context_data(**kwargs)
        context.update(PlayerCardSerializer(self.get_object()).data)
        return context


class PlayerCardIndicators(PlayerCard):
    template_name = 'hockeyapp/players/player-card-indicators.html'


class PlayerCardClubs(PlayerCard):
    template_name = 'hockeyapp/players/player-card-clubs.html'


class PlayerCardCoaches(PlayerCard):
    template_name = 'hockeyapp/players/player-card-coaches.html'


class PlayerCardPartners(PlayerCard):
    template_name = 'hockeyapp/players/player-card-partners.html'


class PlayerCardPhotos(PlayerCard):
    template_name = 'hockeyapp/players/player-card-photos.html'


class PlayerCardCommunication(PlayerCard):
    template_name = 'hockeyapp/players/player-card-communication.html'


class PlayerCardNews(PlayerCard):
    template_name = 'hockeyapp/players/player-card-news.html'


class ClubListView(ListView):
    model = Club
    paginate_by = 100
    template_name = 'hockeyapp/clubs/clubs.html'

    def get_context_data(self, **kwargs):
        context = super(ClubListView, self).get_context_data(**kwargs)
        qs = self.get_queryset()
        page_size = self.get_paginate_by(qs)
        paginator, page, object_list, has_other_pages = self.paginate_queryset(
            qs, page_size)
        context.update({
            'count': qs.count(),
            'results': ClubListSerializer(object_list, many=True).data,
        })
        return context


class ClubView(DetailView):
    model = Club
    template_name = 'hockeyapp/clubs/clubs-calendar.html'

    def get_context_data(self, **kwargs):
        context = super(ClubView, self).get_context_data(**kwargs)
        context.update(ClubSerializer(self.get_object()).data)
        return context


class ClubHomeView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-home.html'


class ClubFanZoneView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-fan.html'


class ClubPhotosView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-photos.html'


class ClubStatsView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-stats.html'
