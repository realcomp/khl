# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, TemplateView
from django.utils.translation import ugettext_lazy as _

from addresses.models import Country

from ..models import Club, Player, ClubPlayer, CoachClub
from ..serializers import (
    CountrySerializer, PlayerCardSerializer, PlayerCardDetailSerializer)
from ..serializers.players import (
    PlayerCardClubsSerializer, PlayerCardCoachesSerializer)


class Index(TemplateView):
    def get_template_names(self):
        version = 'CLASSIC'
        if self.request.user.is_authenticated():

            # TODO: remove it when index template will be competed
            if self.request.user.version == 'PRO':
                return ['hockeyapp/metrics/player-select.html']

            version = self.request.user.version
        return ['hockeyapp/index-%s.html' % version.lower()]
index = Index.as_view()


class IndexClassic(TemplateView):
    version = 'CLASSIC'

    def get_template_names(self):
        return ['hockeyapp/index-%s.html' % self.version.lower()]

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
        return ['hockeyapp/metrics/player-select.html']


class PlayersSearch(TemplateView):
    template_name = 'hockeyapp/players/players-search.html'

    def get_context_data(self, **kwargs):
        context = super(PlayersSearch, self).get_context_data(**kwargs)
        context['request'] = self.request
        countries = (
            Country.objects
            .exclude(ru_title=b'Россия')
            .order_by('%s_title' % self.request.LANGUAGE_CODE))
        context['countries'] = CountrySerializer(
            countries, many=True, context=context).data
        context['russia'] = CountrySerializer(
            Country.objects.filter(ru_title=b'Россия').last(),
            context=context).data
        context['alphabet'] = _('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return context


class PlayerCard(DetailView):
    model = Player
    template_name = 'hockeyapp/players/player-card-short.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerCard, self).get_context_data(**kwargs)
        context['request'] = self.request
        context.update(PlayerCardDetailSerializer(
            self.get_object(), context=context).data)
        return context


class PlayerCardIndicators(PlayerCard):
    template_name = 'hockeyapp/players/player-card-indicators.html'


class PlayerCardClubs(PlayerCard):
    template_name = 'hockeyapp/players/player-card-clubs.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerCardClubs, self).get_context_data(**kwargs)
        clubs = (
            Club.objects
            .filter(clubplayer__player=self.get_object())
            .locale_order_by(self.request, '%s_title').distinct())
        context['clubs'] = PlayerCardClubsSerializer(
            clubs, many=True, context=context).data
        return context


class PlayerCardCoaches(PlayerCard):
    template_name = 'hockeyapp/players/player-card-coaches.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerCardCoaches, self).get_context_data(**kwargs)
        clubplayers = (
            ClubPlayer.objects
            .filter(player=self.get_object())
            .order_by('season__start_date'))
        coaches = {}
        for clubplayer in clubplayers:
            clubcoaches = CoachClub.objects.filter(
                club=clubplayer.club, season=clubplayer.season)
            for clubcoach in clubcoaches:
                pk = clubcoach.coach_id
                if pk not in coaches:
                    coaches[pk] = clubcoach.coach
                if not hasattr(coaches[pk], 'total_days'):
                    coaches[pk].total_days = 0
                duration = clubcoach.end_date - clubcoach.start_date
                coaches[pk].total_days += duration.days
        context['coaches'] = PlayerCardCoachesSerializer(
            coaches.values(), many=True, context=context).data
        return context


class PlayerCardPartners(PlayerCard):
    template_name = 'hockeyapp/players/player-card-partners.html'


class PlayerCardPhotos(PlayerCard):
    template_name = 'hockeyapp/players/player-card-photos.html'


class PlayerCardCommunication(PlayerCard):
    template_name = 'hockeyapp/players/player-card-communication.html'


class PlayerCardNews(PlayerCard):
    template_name = 'hockeyapp/players/player-card-news.html'


class MetricsPlayers(TemplateView):
    template_name = 'hockeyapp/metrics/player-select.html'


class MetricsPlayerCard(PlayerCard):
    model = Player
    template_name = 'hockeyapp/metrics/player-card.html'

    def get_context_data(self, **kwargs):
        context = super(MetricsPlayerCard, self).get_context_data(**kwargs)
        context['request'] = self.request
        context.update(PlayerCardSerializer(
            self.get_object(), context=context).data)
        return context


class MetricsPlayersCompare(TemplateView):
    template_name = 'hockeyapp/metrics/players-diff.html'


class MetricsPlayersCompareGraph(TemplateView):
    template_name = 'hockeyapp/metrics/players-diff3.html'
