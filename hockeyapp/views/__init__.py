# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.utils.translation import ugettext_lazy as _

from addresses.models import Country
from base.models import Season

from ..models import Club, Player, ClubPlayer, CoachClub
from ..serializers import (
    CountrySerializer, SeasonSerializer,
    PlayerCardSerializer, PlayerCardDetailSerializer,
    ClubListSerializer,
)
from ..serializers.players import (
    PlayerCardClubsSerializer, PlayerCardCoachesSerializer)
from ..utils import get_season_end_date


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
        clubplayers = (
            ClubPlayer.objects
            .filter(player=self.get_object())
            .order_by('season__start_date'))
        clubs = {}
        for clubplayer in clubplayers:
            pk = clubplayer.club_id
            if pk not in clubs:
                clubs[pk] = clubplayer.club
            if not hasattr(clubs[pk], 'selected_seasons'):
                clubs[pk].selected_seasons = []
            if clubplayer.season not in clubs[pk].selected_seasons:
                clubs[pk].selected_seasons.append(clubplayer.season)
        context['clubs'] = PlayerCardClubsSerializer(
            clubs.values(), many=True, context=context).data
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


class ClubListView(TemplateView):
    template_name = 'hockeyapp/clubs/clubs.html'

    def get_context_data(self, **kwargs):
        context = super(ClubListView, self).get_context_data(**kwargs)
        year = get_season_end_date().year
        context.update({
            'seasons': map(
                lambda x: (x - 1, x), range(year, year - 10, -1)),
        })
        return context


class ClubView(DetailView):
    model = Club
    template_name = 'hockeyapp/clubs/clubs-team.html'

    def get_context_data(self, **kwargs):
        context = super(ClubView, self).get_context_data(**kwargs)
        context['request'] = self.request
        seasons = (
            Season.objects
            .filter(
                pk__in=self.get_object().clubplayer_set
                .values_list('season_id'))
            .order_by('-start_date'))
        context['seasons'] = SeasonSerializer(
            seasons, context=context, many=True).data
        if 'season' in self.request.GET:
            default_season = get_object_or_404(
                Season, pk=self.request.GET['season'])
        else:
            default_season = seasons[0] if seasons else None
        context['default_season'] = SeasonSerializer(
            default_season, context=context).data
        context.update(ClubListSerializer(
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

    def get_context_data(self, **kwargs):
        context = super(ClubStatsView, self).get_context_data(**kwargs)
        context['alphabet'] = _('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return context


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
