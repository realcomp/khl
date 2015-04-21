# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, TemplateView
from django.utils.translation import ugettext_lazy as _

from rest_framework.renderers import JSONRenderer

from addresses.models import Country

from ..models import Club, Coach, Player, Season
from ..serializers import (
    CountrySerializer, PlayerCardDetailSerializer, SeasonSerializer,
    CountryLeaguesSerializer)
from ..serializers.players import (
    PlayerCardClubsSerializer, PlayerCardCoachesSerializer)


class PlayersSearch(TemplateView):
    template_name = 'hockeyapp/players/players-search.html'

    def get_context_data(self, **kwargs):
        context = super(PlayersSearch, self).get_context_data(**kwargs)
        context['request'] = self.request
        countries = (
            Country.objects
            # .exclude(ru_title=b'Россия')
            .order_by('%s_title' % self.request.LANGUAGE_CODE))
        context['countries'] = CountryLeaguesSerializer(
            countries, context=context, many=True).data
        context['russia'] = CountrySerializer(
            Country.objects.filter(ru_title=b'Россия').last(),
            context=context).data
        context['alphabet'] = _('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        seasons = Season.objects.order_by('-start_date')
        context['seasons'] = SeasonSerializer(
            seasons, context=context, many=True).data
        return context


class PlayersSearch2(PlayersSearch):
    template_name = 'hockeyapp/players/players-search2.html'


class PlayerCard(DetailView):
    model = Player
    template_name = 'hockeyapp/players/player-card-short.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerCard, self).get_context_data(**kwargs)
        context['request'] = self.request
        clubs = Club.objects.active(
                            ).filter(clubplayer__player=self.get_object()
                            ).locale_order_by(self.request, '%s_title'
                            ).distinct()
        context['clubs'] = PlayerCardClubsSerializer(
            clubs, many=True, context=context).data
        context.update(PlayerCardDetailSerializer(
            self.get_object(), context=context).data)
        return context


class PlayerCardIndicators(PlayerCard):
    template_name = 'hockeyapp/players/player-card-indicators.html'


class PlayerCardClubs(PlayerCard):
    template_name = 'hockeyapp/players/player-card-clubs.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerCardClubs, self).get_context_data(**kwargs)
        clubs = Club.objects.active(
                            ).filter(clubplayer__player=self.get_object()
                            ).locale_order_by(self.request, '%s_title'
                            ).distinct()
        context['clubs'] = PlayerCardClubsSerializer(
            clubs, many=True, context=context).data
        return context


class PlayerCardCoaches(PlayerCard):
    template_name = 'hockeyapp/players/player-card-coaches.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerCardCoaches, self).get_context_data(**kwargs)
        clubs = (
            Club.objects
            .filter(clubplayer__player=self.get_object()))
        coaches = (
            Coach.objects
            .filter(coachclub__club__in=clubs, coachclub__head=True)
            .locale_order_by(self.request, '%s_lastname', '%s_name')
            .distinct())
        context['coaches'] = PlayerCardCoachesSerializer(
            coaches, many=True, context=context).data
        return context


class PlayerCardPartners(PlayerCard):
    template_name = 'hockeyapp/players/player-card-partners.html'


class PlayerCardPhotos(PlayerCard):
    template_name = 'hockeyapp/players/player-card-photos.html'


class PlayerCardCommunication(PlayerCard):
    template_name = 'hockeyapp/players/player-card-communication.html'


class PlayerCardNews(PlayerCard):
    template_name = 'hockeyapp/players/player-card-news.html'


class PlayerCardNumbers(PlayerCard):
    template_name = 'hockeyapp/players/player-card-numbers.html'
