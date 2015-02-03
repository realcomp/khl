#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

from django.db import models
from django.db.models import Q
from django.db.models.loading import get_model

from .. import parsers

from . import DataCleanMixin
from ..utils import get_season_start_date, get_season_end_date

CURRENT_APP = __package__.split('.')[0]


class ClubQuerySet(DataCleanMixin, models.QuerySet):
    b''' Менеджер клуба '''
    def _get_data(self, url):
        b''' Берем данные со стороннего сайта парсером '''
        return parsers.club.ClubInfo().get_page(url)

    def create_or_update_club(self, url, update=False, data=None):
        b''' получаем клуб по url со стороннего ресурса '''
        if not data:
            # берем данные о клубе со стороннего ресурса
            data = self._get_data(url)
        ru_title = data.get('ru_title', None)
        if ru_title:
            _club = self.filter(ru_title=ru_title).last()
            if not _club or update:
                if data:
                    data = self.clean_data(data)
                    _logo = data.pop('logo_url', None)
                    if _logo:
                        # создаем фото клуба, если нет в бд
                        data['logo'] = self._get_or_create_image(_logo,
                                                    folder_name='Club logos')
                    _arena = data.pop('arena', None)
                    if _arena:
                        model = get_model(CURRENT_APP, 'Arena')
                        func = model.objects.create_or_update_arena
                        data['arena'] = func(data=_arena,update=True)
                    _coach_fio = data.pop('coach', None)
                    _plrs = data.pop('players', None)
                    if _plrs:
                        model = get_model(CURRENT_APP, 'Player')
                        _plrs = model.objects.filter(khl_id__in=_plrs)
                    if _coach_fio and (not update or _club and not _club.coach):
                        model = get_model(CURRENT_APP, 'Coach')
                        func = model.objects.get_or_create
                        data['coach'] = func(ru_fio=_coach_fio)[0]
                    if update and _club and _club.ru_title:
                        self.filter(ru_title=ru_title).update(**data)
                    else:
                        _club = self.create(**data)
                    _club.players = _plrs
            return _club

    def by_season(self, season):
        '''
        :param season: season years ('2014', '2015')
        :type season: tuple
        '''
        season_start = get_season_start_date(year=season[0])
        season_end = get_season_end_date(year=season[1])
        q_start = (
            Q(leagueclub__start_date__lte=season_start) |
            Q(leagueclub__start_date__isnull=True))
        q_end = (
            Q(leagueclub__end_date__gte=season_end) |
            Q(leagueclub__end_date__isnull=True))
        return self.filter(q_start & q_end)
