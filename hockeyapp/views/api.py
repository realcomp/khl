# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import itertools

from django.db.models import Avg, Q, Sum

from rest_framework import generics, response, viewsets

from addresses.models import Country

from .events import EventFactory
from .mixins import PaginationMixin

from ..filters import PlayersSearchFilter, PlayersSearchOrderFilter
from ..models import Club, Player, ClubPlayerMatch, Schedule, ClubPlayer
from ..models import Timeline

from ..serializers import CountryLeaguesSerializer
from ..serializers import MetricsPlayerSerializer
from ..serializers.clubs import (
    ClubTeamSerializer, ClubTeamCompareSerializer, ClubCalendarSerializer)
from ..serializers.events import EventSerializer
from ..serializers.players import (
    PlayersSearchSerializer, ClubPlayerMatchSerilizer, PlayerNamesSerializer,
    ClubTitlesSerializer)
from ..serializers.timeline import PlayerTimelineSerializer


class PlayersSearch(
        PaginationMixin, viewsets.ReadOnlyModelViewSet):
    filter_backends = PlayersSearchFilter, PlayersSearchOrderFilter
    queryset = Player.objects.all()
    serializer_class = PlayersSearchSerializer

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        self._get_rating(request, qs)

        _pk = request.GET.get('player')
        if _pk:
            _pk = int(_pk)
            # qs is turned into list
            qs = qs.ranged_filter(lambda player: player.pk == _pk, 5)

        instance = qs
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(instance, many=True)
        return response.Response(serializer.data)

    def _get_rating(self, request, qs):
        rated_qs = qs
        rated_by = request.GET.get('rated_by', '')
        if rated_by:
            rated_qs = qs.order_by('-' + rated_by)
        self.rating = {}
        rating_index = 0
        for player in rated_qs:
            if not rated_by:
                rating_index += 1
            self.rating[player.pk] = rating_index


class BestPlayer(PlayersSearch):
    def retrieve(self, request, *args, **kwargs):
        instance = self.filter_queryset(self.get_queryset()).first()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


class PlayerCardIndicators(generics.ListAPIView):
    paginate_by = 99999
    serializer_class = ClubPlayerMatchSerilizer

    def _get_aggregate(self, qs):
        return qs.aggregate(*itertools.chain(
            map(Sum, (
                'plus_minus', 'penalty_time', 'ev_goals', 'pp_goals',
                'es_goals', 'overtime_goals', 'win_goals', 'bullet_goals',
                'shots', 'faceoff', 'winfaceoff', 'winfaceoff_p')),
            map(Avg, (
                'shots', 'pis', 'winfaceoff_p', 'gamingtime',
                'change_count')),
        ))

    def get_queryset(self):
        return ClubPlayerMatch.objects.all()

    def filter_queryset(self, qs):
        qs = super(PlayerCardIndicators, self).filter_queryset(qs)
        _player_id = self.kwargs.get('player_id', 0)

        cp = ClubPlayer.objects.filter(player_id=_player_id)

        if 'season' in self.request.GET:
            cp = cp.filter(season_id=self.request.GET['season'])

        if 'club' in self.request.GET:
            cp = cp.filter(club_id=self.request.GET['club'])

        _coach = self.request.GET.get('coach')
        if _coach:
            cp = cp.filter( club__coachclub__coach_id=_coach,
                            season__coachclub__coach_id=_coach)
        qs = qs.filter(clubplayer__in=cp)

        if self.request.GET.get('group_by') == 'season':
            return qs.group_by_season()
        else:  # group by month (by default)
            return qs.group_by_month()


class PlayerNamesSearch(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerNamesSerializer

    def filter_queryset(self, qs):
        qs = super(PlayerNamesSearch, self).filter_queryset(qs)
        s = self.request.GET.get('s')
        if s:
            qs = qs.filter(**{
                '%s_lastname__istartswith' % self.request.LANGUAGE_CODE: s,
            })
        return qs.order_by('%s_lastname' % self.request.LANGUAGE_CODE)


class PlayerTimeline(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerTimelineSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response.Response({'timeline': serializer.data})


class LeagueList(generics.ListAPIView):
    serializer_class = CountryLeaguesSerializer

    def get_queryset(self):
        return Country.objects.exclude(league__isnull=True)


class ClubTeam(generics.RetrieveAPIView):
    serializer_class = ClubTeamSerializer

    def get_queryset(self):
        return Club.objects.all()


class ClubTeamCompare(generics.RetrieveAPIView):
    serializer_class = ClubTeamCompareSerializer

    def get_queryset(self):
        return Club.objects.all()


class ClubCalendar(generics.ListAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ClubCalendarSerializer

    def filter_queryset(self, qs):
        qs = super(ClubCalendar, self).filter_queryset(qs)
        qs = qs.filter(
            Q(home_team=self.kwargs.get('pk')) |
            Q(guest_team=self.kwargs.get('pk')))
        if 'season' in self.request.GET:
            qs = qs.filter(season=self.request.GET['season'])
        return qs


class MetricsPlayers(generics.ListAPIView):
    paginate_by = 100
    serializer_class = MetricsPlayerSerializer

    def get_queryset(self):
        return Player.objects.all()


class ClubTitlesSearch(generics.ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubTitlesSerializer

    def filter_queryset(self, qs):
        qs = super(ClubTitlesSearch, self).filter_queryset(qs)
        s = self.request.GET.get('s')
        if s:
            qs = qs.filter(**{
                '%s_title__istartswith' % self.request.LANGUAGE_CODE: s,
            })
        return qs.order_by('%s_title' % self.request.LANGUAGE_CODE)


class NewsList(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        efactory = EventFactory(sources={
            'player': Player.objects,
            'schedule': Schedule.objects,
            'timeline': Timeline.objects,
        })
        date = datetime.datetime.now().date()
        if 'date' in self.request.GET:
            date = datetime.datetime.strptime(
                self.request.GET['date'], '%Y-%m-%d').date()
        return efactory.get_events(date)
