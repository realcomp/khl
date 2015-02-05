#coding: utf-8
__author__='smirnov.ev'

import requests

from StringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.loading import get_model

import filer

CURRENT_APP = __package__.split('.')[0]


class DataCleanMixin(object):
    def clean_data(self, data=None):
        data = data or {}
        if data:
            for k,v in data.items():
                if not v:
                    data.pop(k, None)
        return data

    def _get_or_create_image(self, photo_url, folder_name=''):
        b'''создаем в БД фото арены через django-filer
            в папке Arena photos
            В асинхронном режиме не рекомендуется использовать get_or_create
        '''
        response = requests.get(photo_url)
        if response.status_code == 200:
            _buffer = StringIO(response.content)
            img_name = photo_url.split('/')[-1]
            _folder_objects = filer.models.Folder.objects
            folder = _folder_objects.filter(name=folder_name).last()
            if not folder:
                folder = _folder_objects.create(name=folder_name)
            _file_objects = filer.models.Image.objects
            data = dict(folder=folder,
                        name=img_name,
                        is_public=True
            )
            _file = _file_objects.filter(**data).last()
            if not _file:
                _file = _file_objects.create(**data)
            _file.file.save(img_name,
                            InMemoryUploadedFile(_buffer, "image", img_name, 
                            None, _buffer.tell(), None)
            )
            _file.save()
            return _file


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
        for m in kwargs.get('matches',):
            _match = self.filter(khl_id = m.get('khl_id')).last()
            m['league'] = _league
            m['season'] = _season
            m['home_team'] = self._get_team(m.pop('home_team', None))
            m['guest_team'] = self._get_team(m.pop('guest_team', None))
            if _match and _match.ru_title == m.get('ru_title'):
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
        self.filter(league=_league, season=_season, khl_id__isnull=True
            ).update(is_championship=False)
        self.filter(league=_league, season=_season, khl_id__isnull=False
            ).update(is_championship=True)
        for m in kwargs.get('matches',):
            home_team= self._get_team(m.pop('home_team', None))
            guest_team= self._get_team(m.pop('guest_team', None))
            _match = self.filter(ru_title = m.get('ru_title'),
                                league = _league,
                                season = _season,
                                home_team = home_team,
                                guest_team = guest_team,
                                khl_id__isnull=True,
                        ).last()
            if _match:
                m['is_championship'] = True
                if not _match.match and m.get('khl_id'):
                    _model = get_model(CURRENT_APP, 'Match')
                    _m = _model.objects.filter(khl_id=m.get('khl_id')).last()
                    if _m:
                        m['match'] = _m
                        m['processed'] = True
                        _m.is_championship = _match.is_championship
                        _m.is_playoff = _match.is_playoff
                        _m.save(update_fields=['is_playoff', 'is_championship'])
                self.filter(pk=_match.pk).update(**m)

    def _get_team(self, ru_title):
        club_model = get_model(CURRENT_APP, 'club')
        _club = club_model.objects.by_title_alias(ru_title).first()
        if not _club:
            _club = club_model.objects.get_or_create(ru_title=ru_title)
        return _club


from . import arena, club, match, player