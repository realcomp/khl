#coding: utf-8
__author__='smirnov.ev'

from django.db import models
from django.db.models.loading import get_model

from base.managers import GetFilerImage

CURRENT_APP = __package__.split('.')[0]


class DataCleanMixin(GetFilerImage):
    def clean_data(self, data=None):
        data = data or {}
        if data:
            for k,v in data.items():
                if not v:
                    data.pop(k, None)
        return data


class ScheduleManager(models.Manager):
    b''' Мененжер календаря матчей по-умолчанию '''
    def create_schedule(self, **kwargs):
        b''' метод взять или создать записи о матчах '''
        _season = kwargs.pop('season', {})
        _league = kwargs.pop('league', 'KHL')
        sm = get_model('base', 'Season')
        _season, _crt = sm.objects.get_or_create_season(**_season)
        league_model = get_model(CURRENT_APP, 'League')
        _league, _crt = league_model.objects.get_or_create(en_title=_league)
        challenge_type = kwargs.pop('challenge_type', None)
        for m in kwargs.get('matches',):
            _match = self.filter(khl_id = m.get('khl_id')).last()
            m['league'] = _league
            m['season'] = _season
            m['home_team'] = self._get_team(m.pop('home_team', None))
            m['guest_team'] = self._get_team(m.pop('guest_team', None))
            m['challenge_type'] = challenge_type
            if m.get('khl_id') and (not _match or not _match.match):
                m['match'] = self._get_match(m)
                m['processed'] = True
            if _match and _match.title == m.get('title'):
                self.filter(pk=_match.pk).update(**m)
            else:
                self.create(**m)

    def update_schedule(self, **kwargs):
        b''' метод обновить записи о матчах '''
        _season = kwargs.pop('season', {})
        _league = kwargs.pop('league', 'KHL')
        sm = get_model('base', 'Season')
        _season, _crt = sm.objects.get_or_create_season(**_season)
        league_model = get_model(CURRENT_APP, 'League')
        _league, _crt = league_model.objects.get_or_create(en_title=_league)
        challenge_type = kwargs.pop('challenge_type', None)
        for m in kwargs.get('matches',):
            home_team= self._get_team(m.pop('home_team', None))
            guest_team= self._get_team(m.pop('guest_team', None))
            qs = dict(  title = m.get('title'),
                        league = _league,
                        season = _season,
                        home_team = home_team,
                        guest_team = guest_team,
            )
            if kwargs.get('without_khl_id', True):
                qs['khl_id__isnull'] = True
            _match = self.filter(**qs).last()
            if _match:
                m['challenge_type'] = challenge_type
                if not _match.match and m.get('khl_id'):
                    _m = self._get_match(m)
                    m['match'] = _m
                    m['processed'] = True
                self.filter(pk=_match.pk).update(**m)

    def _get_team(self, title):
        club_model = get_model(CURRENT_APP, 'club')
        _club = club_model.objects.by_title_alias(title).first()
        if not _club:
            _club = club_model.objects.get_or_create(title=title)
        return _club

    def _get_match(self, m=None):
        _model = get_model(CURRENT_APP, 'Match')
        _m = _model.objects.filter(khl_id=m.get('khl_id')).last()
        if _m and m:
            _m.challenge_type = m.get('challenge_type')
            _m.save()
        return _m

from . import arena, club, match, player