#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

from django.db import models

from . import DataCleanMixin


class ArenaQuerySet(DataCleanMixin, models.QuerySet):
    b''' Менеджер арены '''
    def create_or_update_arena(self, update=False, data=None):
        b''' Создание или обновление арены '''
        title = data.get('title', None)
        if title:
            _arena = self.filter(title=title).last()
            if data:
                data = self.clean_data(data)
                _logo = data.pop('photo_url', None)
                if _logo:
                    # создаем фото клуба, если нет в бд
                    data['photo'] = self._get_or_create_image(_logo, 
                                                folder_name='Arena photos')
                if update and _arena:
                    self.filter(title=title).update(**data)
                else:
                    _arena = self.create(**data)
            return _arena

class ArenaInstaPhotoQuerySet(DataCleanMixin, models.QuerySet):
    b''' Менеджер инстаграмм фото арены '''
    def to_view(self):
        b''' прошедшие модерацию фото '''
        return self.filter(processed=True)

    def for_moderation(self):
        b''' непрошедшие модерацию фото '''
        return self.filter(processed=False)

    def arena_photo(self, arena):
        return self.to_view().filter(arena=arena)

    def club_photo(self, club):
        return self.to_view().filter(club=club)

    def player_photo(self, player):
        return self.to_view().filter(player__in=(player,))