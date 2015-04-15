# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import itertools

from django.db.models import Avg, Q, Sum
from django.shortcuts import get_object_or_404

from rest_framework import generics, response, viewsets

from base.models import Season

from ..events import EventFactory
from ..mixins import PaginationMixin

from ...filters import PlayersSearchFilter, PlayersSearchOrderFilter
from ...models import Club, Player, ClubPlayerMatch, Schedule, ClubPlayer
from ...models import Timeline

from ...serializers import MetricsPlayerSerializer
from ...serializers.clubs import (
    ClubTeamSerializer, ClubTeamCompareSerializer, ClubCalendarSerializer,
    ClubCalendarPaginationSerializer)
from ...serializers.events import EventSerializer
from ...serializers.players import (
    PlayersSearchSerializer, ClubPlayerMatchSerilizer, PlayerNamesSerializer,
    ClubTitlesSerializer, ClubPlayerMatchPaginationSerilizer,
    ClubPlayerNumbersSerializer, PlayerNumbersSerializer)
from ...serializers.schedule import ScheduleSerializer
from ...serializers.timeline import PlayerTimelineSerializer


class PlayersSearch(PaginationMixin, viewsets.ReadOnlyModelViewSet):
    filter_backends = PlayersSearchFilter, PlayersSearchOrderFilter
    queryset = Player.objects.all()
    serializer_class = PlayersSearchSerializer

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        self.rating = self._get_rating(request, qs)

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
        result = {}
        rating_index = 0
        if not request.GET.get('rated_by', ''):
            for player in qs:
                rating_index += 1
                result[player.pk] = rating_index
        return result


class BestPlayer(PlayersSearch):
    def retrieve(self, request, *args, **kwargs):
        instance = self.filter_queryset(self.get_queryset()).first()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


class PlayerCardIndicators(generics.ListAPIView):
    queryset = ClubPlayerMatch.objects.all()
    paginate_by = 99999
    pagination_serializer_class = ClubPlayerMatchPaginationSerilizer
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


class ClubTeam(generics.RetrieveAPIView):
    serializer_class = ClubTeamSerializer

    def get_queryset(self):
        return Club.objects.active()


class ClubTeamCompare(generics.RetrieveAPIView):
    serializer_class = ClubTeamCompareSerializer

    def get_queryset(self):
        return Club.objects.active()


class ClubCalendar(generics.ListAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ClubCalendarSerializer
    paginate_by = 99999
    pagination_serializer_class = ClubCalendarPaginationSerializer

    def filter_queryset(self, qs):
        qs = super(ClubCalendar, self).filter_queryset(qs)
        qs = qs.filter(
            Q(home_team=self.kwargs.get('pk')) |
            Q(guest_team=self.kwargs.get('pk')))
        if 'season' in self.request.GET:
            qs = qs.filter(season=self.request.GET['season'])
        return qs

    def list(self, request, *args, **kwargs):
        self.season = get_object_or_404(
            Season, pk=self.request.GET.get('season', 0))
        return super(ClubCalendar, self).list(request, *args, **kwargs)


class MetricsPlayers(generics.ListAPIView):
    paginate_by = 100
    serializer_class = MetricsPlayerSerializer

    def get_queryset(self):
        return Player.objects.all()


class ClubTitlesSearch(generics.ListAPIView):
    queryset = Club.objects.active()
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


class ScheduleView(generics.RetrieveAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class NumbersList(generics.ListAPIView):
    queryset = ClubPlayer.objects.all()


class ClubPlayerNumbers(NumbersList):
    serializer_class = ClubPlayerNumbersSerializer

    def filter_queryset(self, qs):
        qs = super(ClubPlayerNumbers, self).filter_queryset(qs)

        _club = self.request.GET.get('club')
        if _club:
            qs = qs.filter(club=_club)

        players_by_number = {}
        for clubplayer in qs.order_by('season__start_date'):
            player = clubplayer.player
            number = clubplayer.number
            if number not in players_by_number:
                players_by_number[number] = {
                    'players': [],
                    'number': int(number or 0),
                }
            if player not in players_by_number[number]['players']:
                players_by_number[number]['players'].append(player)

        return sorted(players_by_number.values(), key=lambda x: x['number'])


class PlayerNumbers(NumbersList):
    serializer_class = PlayerNumbersSerializer

    def filter_queryset(self, qs):
        qs = super(PlayerNumbers, self).filter_queryset(qs)

        _player = self.request.GET.get('player')
        if _player:
            qs = qs.filter(player=_player)

        clubs_by_number = {}
        for clubplayer in qs.order_by('season__start_date'):
            club = clubplayer.club
            number = clubplayer.number
            if number not in clubs_by_number:
                clubs_by_number[number] = {
                    'clubs': [],
                    'number': int(number or 0),
                }
            if club not in clubs_by_number[number]['clubs']:
                clubs_by_number[number]['clubs'].append(club)

        return sorted(clubs_by_number.values(), key=lambda x: x['number'])
