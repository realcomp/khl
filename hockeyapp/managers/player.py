#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

import requests

from PIL import Image
from StringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

import filer

from addresses.models import Country


class PlayerQuerySet(models.QuerySet):
    b''' Менеджер игрока '''
    def get_or_create_player(self, khl_id, fio='', update=False, data=None):
        b''' получаем игрока по id со стороннего ресурса '''
        _player = self.filter(khl_id=khl_id).last()
        if not _player or update:
            if data:
                #clear data ####################################################
                for k,v in data.items(): 
                    if not v: 
                        data.pop(k, None)
                ################################################################
                data.pop('club', None)
                _ava = data.pop('ava_url', None)
                if _ava:
                    # создаем фото игрока, если нет в бд
                    data['photo'] = self._create_photo(khl_id, _ava)
                _citizenship = data.pop('citizenship', None)
                if _citizenship:
                    _func = Country.objects.get_or_create
                    data['citizenship'], _crt = _func(ru_title = _citizenship)
                if not data.get('fio') and fio:
                    data['fio'] = fio
            else:
                data = dict(khl_id=khl_id,)
                if fio:
                    data['fio']=fio
            if update and _player:
                self.filter(khl_id=_player.khl_id).update(**data)
            else:
                _player = self.create(**data)
        return _player

    def _create_photo(self, khl_id, ava_url):
        b'''создаем в БД фото игрока через django-filer
            в папке players
            В асинхронном режиме не рекомендуется использовать get_or_create
        '''
        response = requests.get(ava_url)
        if response.status_code == 200:
            _buffer = StringIO(response.content)
            img = Image.open(_buffer)
            img_name = '{}.{}'.format(khl_id,img.format)
            _folder_objects = filer.models.Folder.objects
            folder = _folder_objects.filter(name='Player photo').last()
            if not folder:
                folder = _folder_objects.create(name='Player photo')
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

    def ranged_filter(self, filter_, range_):
        i = 0
        start = 0
        end = 0
        count = self.count()
        for obj in self:
            if filter_(obj):
                break
            i += 1
        start = i - range_
        end = i + range_
        if i - range_ < 0:
            start = 0
            end = i + range_
            end -= i - range_
        elif i + range_ > count - 1:
            end = count - 1
            start = i - range_
            start += (count - 1) - (i + range_)
        return self[start:end + 1]

    # def by_season(self, club, season=None):
    #     '''
    #     :param season: season years ('2014', '2015')
    #     :type season: tuple
    #     '''
    #     club_players = club.clubplayer_set
    #     if season:
    #         season_start = get_season_start_date(year=season[0])
    #         season_end = get_season_end_date(year=season[1])
    #         q_start = Q(start_date__lte=season_start)
    #         q_end = Q(end_date__gte=season_end) | Q(end_date__isnull=True)
    #         club_players = club_players.filter(q_start & q_end)
    #     player_ids = club_players.values_list('player_id', flat=True)
    #     return self.filter(pk__in=player_ids)


class ClubPlayerQuerySet(models.QuerySet):
    def by_season(self, season):
        qs = self.filter(season=season)
        # if season.is_last:
        #     end_date = min(datetime.datetime.now().date(), season.end_date)
        #     qs = qs.filter(end_date__gte=end_date)
        return qs

    def by_leagues(self, leagues):
        return self.filter(league__in=leagues)