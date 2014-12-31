# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, TemplateView

from ..serializers import (
    ClubListSerializer, ClubSerializer, PlayerCardSerializer)
from ..models import Club, Player


class PlayersSearch(TemplateView):
    template_name = 'hockeyapp/players/players-search.html'


class PlayerCard(DetailView):
    model = Player
    template_name = 'hockeyapp/players/player-card-short.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerCard, self).get_context_data(**kwargs)
        context['request'] = self.request
        context.update(PlayerCardSerializer(
            self.get_object(), context=context).data)
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


class ClubListView(TemplateView):
    template_name = 'hockeyapp/clubs/clubs.html'

    def get_context_data(self, **kwargs):
        context = super(ClubListView, self).get_context_data(**kwargs)
        context.update({
            'club_types': (
                'clubs-all', 'clubs-chl', 'clubs-nhl', 'clubs-vhl',
                'clubs-mhl', 'clubs-mhla'),
        })
        return context


class ClubView(DetailView):
    model = Club
    template_name = 'hockeyapp/clubs/clubs-team.html'

    def get_context_data(self, **kwargs):
        context = super(ClubView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context.update(ClubSerializer(
            self.get_object(), context=context).data)
        return context


class ClubCalendarView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-calendar.html'


class ClubHomeView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-home.html'


class ClubFanZoneView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-fan.html'


class ClubPhotosView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-photos.html'


class ClubStatsView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-stats.html'


class MetricsPlayers(TemplateView):
    template_name = 'hockeyapp/metrics/player-select.html'


class MetricsPlayerCard(PlayerCard):
    template_name = 'hockeyapp/metrics/player-card.html'


class MetricsPlayersCompare(TemplateView):
    template_name = 'hockeyapp/metrics/players-diff.html'


class MetricsPlayersCompare2(TemplateView):
    template_name = 'hockeyapp/metrics/players-diff2.html'


class MetricsPlayersCompare3(TemplateView):
    template_name = 'hockeyapp/metrics/players-diff3.html'
