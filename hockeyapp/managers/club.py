#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

from django.db import models
from django.db.models import Q
from django.db.models.loading import get_model

from .. import parsers

from . import DataCleanMixin, LocaleOrderMixin

CURRENT_APP = __package__.split('.')[0]


class ClubQuerySet(LocaleOrderMixin, DataCleanMixin, models.QuerySet):
    b''' Менеджер клуба '''
    def _get_data(self, url):
        b''' Берем данные со стороннего сайта парсером '''
        return parsers.club.ClubInfo().get_page(url)

    def create_or_update_club(self, url, update=False, data=None):
        b''' получаем клуб по url со стороннего ресурса '''
        if not data:
            # берем данные о клубе со стороннего ресурса
            data = self._get_data(url)
        title = data.get('title', None)
        # TODO: refact
        if data.get('league') and data.get('league').en_title == 'VHL':
            if title == 'Динамо': title+= ' Бшх'
        if title:
            _club = self.by_title_alias(title).last()
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
                        data['coach'] = func(fio=_coach_fio)[0]
                    if update and _club and _club.title:
                        if _club.logo: data.pop('logo', None)
                        self.filter(title=title).update(**data)
                    else:
                        _club = self.create(**data)
                    if _plrs:
                        _club.players = _plrs
            return _club

    def by_season(self, season):
        return self.active().filter(leagueclub__season=season)

    def by_title_alias(self, title):
        q_title = ( Q(ru_title=title) |
                    Q(en_title=title)
        )
        q_title|= ( Q(clubtitlealias__alias__ru_title=title) |
                    Q(clubtitlealias__alias__en_title=title)
        )
        return self.active().filter(q_title)

    def active(self):
        return self.exclude(league__en_title="Not clubs")

    def not_active(self):
        return self.filter(league__en_title="Not clubs")

    def recalc_counters(self, fields, update_last_match_date=False):
        for club in self:
            q_not_parsed_yet = Q(date__gt=club.last_match_date)

            if (not club.last_match_date or
                    club.homematches.filter(q_not_parsed_yet).exists() or
                    club.guestmatches.filter(q_not_parsed_yet).exists() or
                    (not club.homematches.exists() and not club.guestmatches.exists())):

                for field in fields:
                    value = None
                    if field == 'matches_total':
                        value = (
                            club.homematches.count() +
                            club.guestmatches.count())

                    setattr(club, field, value)

                update_fields = list(fields)
                if update_last_match_date:
                    last_match = None
                    last_homematch = club.homematches.order_by('date').last()
                    last_guestmatch = club.guestmatches.order_by('date').last()
                    if last_homematch and last_guestmatch:
                        return max(
                            (last_homematch, last_guestmatch),
                            key=lambda x: x.date)
                    else:
                        last_match = last_homematch or last_guestmatch
                    if last_match:
                        club.last_match_date = last_match.date
                        update_fields = update_fields + ['last_match_date']

                club.save(update_fields=update_fields)
        return self
