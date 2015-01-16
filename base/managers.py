#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

from django.db import models


class SeasonManager(models.Manager):
    b''' Менеджер сезонов '''
    def get_or_create_season(self, start_date, end_date):
        ru_title = '{} {}/{}'.format(   'Сезон',
                                        start_date.strftime('%y'),
                                        end_date.strftime('%y'),
        )
        en_title = '{} {}/{}'.format(  'Season',
                                        start_date.strftime('%y'),
                                        end_date.strftime('%y'),
        )
        data = dict(ru_title=ru_title,en_title=en_title,start_date=start_date,
                    end_date=end_date)
        return self.get_or_create(**data)