# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import itertools

from django.db.models import Avg, Q, Sum
from django.shortcuts import get_object_or_404

from rest_framework import generics, response, viewsets

from base.models import Season

from ..events import EventFactory

from ...filters import PlayersSearchFilter, PlayersSearchOrderFilter
from ...models import Club, Player, ClubPlayerMatch, Schedule, ClubPlayer
from ...models import Timeline, PlayerSeasonStat

from ...serializers import MetricsPlayerSerializer
from ...serializers.clubs import (
    ClubTeamSerializer, ClubTeamCompareSerializer, ClubCalendarSerializer,
    ClubCalendarPagination)
from ...serializers.events import EventSerializer
from ...serializers.players import (
    PlayersSearchSerializer, ClubPlayerMatchSerilizer, PlayerNamesSerializer,
    ClubTitlesSerializer, ClubPlayerMatchPagination)
from ...serializers.schedule import ScheduleSerializer
from ...serializers.timeline import PlayerTimelineSerializer


class _ZeroCountProxy(object):
    def count(self):
        return 0


class PlayerSeasonStatProxy(object):
    """
    Mimics the ClubPlayerMatch queryset interface expected by
    ClubPlayerMatchSerilizer. Wraps one or more PlayerSeasonStat records
    for a single season so they can be serialized alongside match-based data.
    """
    def __init__(self, stats, season):
        self._stats = stats
        self.season = season
        self.start_date = season.start_date if season else None
        self.end_date = season.end_date if season else None
        self.date = None

    def _total(self, field):
        vals = [getattr(s, field) for s in self._stats
                if getattr(s, field, None) is not None]
        return sum(vals) if vals else None

    def _avg(self, field):
        vals = [getattr(s, field) for s in self._stats
                if getattr(s, field, None) is not None]
        return (sum(vals) / len(vals)) if vals else None

    def count(self):
        return sum(s.matches or 0 for s in self._stats)

    def aggregate(self, *args, **kwargs):
        if getattr(self, '_agg_cache', None) is None:
            self._agg_cache = {
                'plus_minus__sum': self._total('plus_minus'),
                'penalty_time__sum': self._total('penalty_time'),
                'ev_goals__sum': self._total('ev_goals'),
                'pp_goals__sum': self._total('pp_goals'),
                'es_goals__sum': self._total('es_goals'),
                'overtime_goals__sum': self._total('overtime_goals'),
                'win_goals__sum': self._total('win_goals'),
                'bullet_goals__sum': self._total('bullet_goals'),
                'shots__sum': self._total('shots'),
                'faceoff__sum': self._total('faceoff'),
                'winfaceoff__sum': self._total('winfaceoff'),
                'winfaceoff_p__sum': self._total('winfaceoff_p'),
                'goals__sum': self._total('goals'),
                'assists__sum': self._total('assists'),
                'points__sum': self._total('points'),
                'loose_goals__sum': self._total('loose_goals'),
                'saves__sum': self._total('saves'),
                'shots__avg': self._avg('shots_per_game'),
                'pis__avg': self._avg('pis'),
                'winfaceoff_p__avg': self._avg('winfaceoff_p'),
                'saves_p__avg': self._avg('saves_p'),
                'sf__avg': self._avg('sf'),
                'adv_stats__gamingtime_all__avg': None,
                'gamingtime__avg': None,
                'adv_stats__change_count_all__avg': None,
                'change_count__avg': None,
            }
        return self._agg_cache

    def filter(self, *args, **kwargs):
        return _ZeroCountProxy()

    def home_matches_win(self):
        return _ZeroCountProxy()

    def guest_matches_win(self):
        return _ZeroCountProxy()

    def home_matches_lose(self):
        return _ZeroCountProxy()

    def guest_matches_lose(self):
        return _ZeroCountProxy()


class PlayerCardIndicators(generics.ListAPIView):
    queryset = ClubPlayerMatch.objects.all()
    paginate_by = 99999
    pagination_class = ClubPlayerMatchPagination
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
            match_seasons = list(qs.group_by_season())
            covered_season_ids = {
                s.season.pk for s in match_seasons if s.season
            }

            season_stats_qs = PlayerSeasonStat.objects.filter(
                player_id=_player_id,
            ).select_related('season', 'club').order_by('season__start_date')

            if 'season' in self.request.GET:
                season_stats_qs = season_stats_qs.filter(
                    season_id=self.request.GET['season'])

            stats_by_season = {}
            for stat in season_stats_qs:
                if stat.season_id not in covered_season_ids and stat.season:
                    stats_by_season.setdefault(stat.season_id, []).append(stat)

            additional = [
                PlayerSeasonStatProxy(stats, stats[0].season)
                for stats in stats_by_season.values()
            ]

            all_results = match_seasons + additional
            all_results.sort(key=lambda x: (
                x.season.start_date
                if x.season and x.season.start_date
                else datetime.date(1900, 1, 1)
            ))
            return all_results
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
    paginate_by = 99999
    pagination_class = ClubCalendarPagination
    serializer_class = ClubCalendarSerializer

    def filter_queryset(self, qs):
        qs = super(ClubCalendar, self).filter_queryset(qs)
        qs = qs.filter(
            Q(home_team=self.kwargs.get('pk')) |
            Q(guest_team=self.kwargs.get('pk')))
        if 'season' in self.request.GET:
            qs = qs.filter(season=self.request.GET['season'])
        return qs

    def list(self, request, *args, **kwargs):
        # self.season = get_object_or_404(
        #     Season, pk=self.request.GET.get('season', 0))
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
