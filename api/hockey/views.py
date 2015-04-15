# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import collections
import rest_framework as drf

from django.db.models import Q

from base.models import Season
from hockeyapp.filters import OrderFilter
from hockeyapp.views.mixins import PaginationMixin
from hockeyapp.models import Club, Country, Player, League, LeagueClub, Match

from .admin import ArenaInstaPhotoList
from .serializers import ClubListSerializer, PlayerPartnersBySeasonCount
from .serializers import PlayerPartnersBySeason, ClubListPaginationSerializer
from .serializers import MatchListSerializer


class ClubInstaPhotoList(ArenaInstaPhotoList):
    b''' прошедшие модерацию инстаграмм фото клуба '''
    permission_classes = ()
    def filter_queryset(self, qs):
        processed = self.request.GET.get('processed')
        if processed:
            return super(ClubInstaPhotoList, self).filter_queryset(qs)
        else:
            return qs.none()
cip_list = ClubInstaPhotoList.as_view()


class PlayerInstaPhotoList(ClubInstaPhotoList):
    b''' прошедшие модерацию инстаграмм фото игрока '''
    def filter_queryset(self, qs):
        qs = super(PlayerInstaPhotoList, self).filter_queryset(qs)
        if self.request.GET.get('player'):
            qs = qs.player_photo(self.request.GET.get('player'))
        return qs
pip_list = PlayerInstaPhotoList.as_view()


class ProcessedArenaInstaPhotoList(ClubInstaPhotoList):
    b''' прошедшие модерацию инстаграмм фото арены '''
    def filter_queryset(self, qs):
        qs = super(ProcessedArenaInstaPhotoList, self).filter_queryset(qs)
        if self.request.GET.get('arena'):
            qs = qs.arena_photo(self.request.GET.get('arena'))
        return qs
paip_list = ProcessedArenaInstaPhotoList.as_view()


class ClubList(PaginationMixin, drf.generics.ListAPIView):
    filter_backends = OrderFilter,
    serializer_class = ClubListSerializer
    pagination_serializer_class = ClubListPaginationSerializer

    def _get_season(self):
        default = Season.objects.latest('start_date')
        return self.request.GET.get('season', default)

    def _get_leagues(self):
        leagueclubs = LeagueClub.objects.filter(season=self._get_season())
        return League.objects.filter(pk__in=leagueclubs.values_list('league'))

    def _get_league(self):
        if 'league' in self.request.GET:
            league = self.request.GET['league']
            if league:  # selected
                return League.objects.get(pk=league)
            else:  # default
                leagues = self._get_leagues()
                khl = leagues.filter(ru_title='КХЛ')
                if khl.exists():
                    return khl.last()
                superleague = leagues.filter(ru_title='Суперлига')
                if superleague.exists():
                    return superleague.last()
                return leagues.last()

    def get_queryset(self):
        return Club.objects.active()

    def filter_queryset(self, qs):
        qs = super(ClubList, self).filter_queryset(qs)
        q = Q()
        if 'country' in self.request.GET:
            country = Country.objects.filter(pk=self.request.GET['country']
                                    ).last()
        else:
            country = Country.objects.filter(ru_title=b'Россия'
                                    ).last()
        if country:
            q &= Q(leagueclub__league__country_id=country)

        if 'league' in self.request.GET:
            q &= Q(leagueclub__league=self._get_league())

        q &= Q(leagueclub__season=self._get_season())

        ids = set(qs.filter(q).values_list('pk', flat=True))
        qs = qs.filter(pk__in=ids)
        return qs
club_list = ClubList.as_view()


class PlayerPartners(drf.generics.ListAPIView):
    serializer_class = PlayerPartnersBySeasonCount
    _plrs_seasons = None

    def get_queryset(self):
        if self.kwargs.get('player_id'):
            return Player.objects.all()
        else:
            return Player.objects.none()

    def get_serializer_class(self):
        _rate_by = self.request.GET.get('rate_by')
        if _rate_by:
            return PlayerPartnersBySeason
        return self.serializer_class

    def filter_queryset(self, qs):
        _player_id = self.kwargs.get('player_id')
        qs = super(PlayerPartners, self).filter_queryset(qs)
        _is_playing = self.request.GET.get('is_playing')
        if _is_playing:
            qs = qs.filter(clubplayer__season=Season.objects.latest('start_date'))
        if not self._plrs_seasons:
            cp = qs.filter(pk=_player_id)
            _club_season = cp.filter(clubplayer__season__isnull=False
                            ).values_list(  'clubplayer__club_id',
                                            'clubplayer__season_id',)
            self._plrs_seasons = self._get_players_by_season(qs,_club_season)
            _plrs_ids = frozenset().union(*self._plrs_seasons.values())
        qs = qs.filter(pk__in = _plrs_ids).exclude(pk=_player_id)
        return qs

    def _get_players_by_season(self, qs, club_season):
        b'''Группируем id игроков по сезонам'''
        _plrs_by_season = dict()
        for club, season in club_season:
            prtnrs = qs.filter( clubplayer__club_id=club,
                                clubplayer__season_id=season
                        ).values_list('pk', flat=True)
            prtnrs = set(prtnrs)
            if _plrs_by_season.get(season):
                _plrs_by_season[season] = _plrs_by_season[season] | set(prtnrs)
            else:
                _plrs_by_season[season] = set(prtnrs)
        return _plrs_by_season

    def _get_partner_ids_with_season_count(self, qs):
        b'''Получаем словарь id_игрока: кол-во сезонов,
            проведенных с данным игроком
        '''
        _plrs_seasons = collections.Counter()
        map(_plrs_seasons.update, self._plrs_seasons.values())
        return _plrs_seasons

    def _group_by_both_seasons(self, qs):
        b'''Группируем id игроков по количеству сезонов,
            проведенных с данным игроком
        '''
        if qs.exists():
            _plrs_seasons = self._get_partner_ids_with_season_count(qs)
            instance = collections.OrderedDict()
            for plr in qs:
                count = _plrs_seasons.get(plr.pk)
                if count:
                    if instance.get(count):
                        instance[count].append(plr)
                    else:
                        instance[count] = [plr,]
            return reversed(instance.items())
        return qs

    def _group_by_early_season(self, qs):
        b'''Группируем id игроков по сезонe,
            проведенных с данным игроком, начиная с самого раннего
        '''
        if qs.exists():
            seasons = Season.objects.filter(pk__in=self._plrs_seasons.keys()
                                    ).order_by('start_date')
            players = set(qs)
            res = []
            for season in seasons:
                plr_ids = self._plrs_seasons.get(season.pk)
                _plrs = [obj for obj in players if obj.pk in plr_ids]
                res.append((season, _plrs))
            return res
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        _rate_by = request.GET.get('rate_by')
        if _rate_by:
            instance = self._group_by_early_season(qs)
        else:
            instance = self._group_by_both_seasons(qs)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(instance, many=True)
        return drf.response.Response(serializer.data)
player_partners = PlayerPartners.as_view()


class MatchList(drf.generics.ListAPIView):
    serializer_class = MatchListSerializer

    def get_queryset(self):
        return Match.objects.active().order_by('-date')

    def filter_queryset(self, qs):
        qs = super(MatchList, self).filter_queryset(qs)
        club_id = self.request.GET.get('club')
        if club_id:
            q = Q(home_team_id=club_id) | Q(guest_team_id=club_id)
            season_id = self.request.GET.get('season')
            if season_id:
                season = Season.objects.filter(id=season_id).last()
                q&= Q(date__gte=season.start_date, date__lte=season.end_date)
            ids = set(qs.filter(q).values_list('pk', flat=True))
            qs = qs.filter(pk__in=ids)
            return qs
        return qs.none()
matches = MatchList.as_view()