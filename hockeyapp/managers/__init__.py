#coding: utf-8
__author__='smirnov.ev'

from django.conf import settings
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

    def create_or_update_schedule(self, **kwargs):
        b''' метод взять или создать или обновить записи о матчах '''
        _season = self._get_season(kwargs.pop('season', {}))
        _league = self._get_league(kwargs.pop('league', 'KHL'))
        challenge_type = kwargs.pop('challenge_type', None)
        challenge = kwargs.pop('challenge', None)
        for m in kwargs.get('matches',):
            _home_team = self._get_team(m.pop('home_team', None))
            _guest_team= self._get_team(m.pop('guest_team', None))
            qs = dict(  title = m['title'].encode('utf-8'),
                        league = _league,
                        season = _season,
                        home_team = _home_team,
                        guest_team = _guest_team,
                        challenge = challenge,
                        challenge_type = challenge_type,
            )
            if m.get('khl_id'):
                qs['khl_id'] = m.get('khl_id')
                m['match'] = self._get_match(m)
                if m['match']: m['processed'] = True
            m.update(qs)
            _match = self.filter(**qs).last()
            if _match:
                self.filter(pk=_match.pk).update(**m)
            else:
                self.create(**m)

    def _get_season(self, season):
        sm = get_model('base', 'Season')
        _season, _crt = sm.objects.get_or_create_season(**season)
        return _season

    def _get_league(self, league):
        league_model = get_model(CURRENT_APP, 'League')
        _league, _crt = league_model.objects.get_or_create(en_title=league)
        return _league

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
            _m.save(update_fields=['challenge_type'])
        return _m


class LocaleOrderMixin(object):
    def locale_order_by(self, request, *args):
        if request:
            lc = getattr(request, 'LANGUAGE_CODE')
            if lc in zip(*settings.LANGUAGES)[0]:
                args = map(lambda x: x % lc if '%s' in x else x, args)
        return self.order_by(*args)


from . import arena, club, match, player
