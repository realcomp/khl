#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

from django.db import models

from . import DataCleanMixin


class ArenaManager(DataCleanMixin, models.Manager):
    b''' Менеджер арены '''
    def create_or_update_arena(self, update=False, data=None):
        b''' Создание или обновление арены '''
        ru_title = data.get('ru_title', None)
        if ru_title:
            _club = self.filter(ru_title=ru_title).last()
            if not _club or update:
                if data:
                    data = self.clean_data(data)
                    _logo = data.pop('photo_url', None)
                    if _logo:
                        # создаем фото клуба, если нет в бд
                        data['photo'] = self._get_or_create_image(_logo, 
                                                    folder_name='Arena photos')
                    if update and _club:
                        self.filter(ru_title=ru_title).update(**data)
                    else:
                        _club = self.create(**data)
            return _club