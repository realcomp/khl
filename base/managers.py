#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

import datetime
import requests

from StringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile

from django.db import models

import filer


class GetFilerImage(object):
    def _get_or_create_image(self, photo_url, folder_name=''):
        b'''создаем в БД фото через django-filer
            в папке folder_name
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


class SeasonQuerySet(models.QuerySet):
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

    def active(self):
        ''' skip future seasons '''
        return self.filter(start_date__lte=datetime.datetime.now().date())


class IIFQuerySet(GetFilerImage, models.QuerySet):
    b''' Менеджер инстаграм изображений '''
    def get_or_create_iif(self, iif_obj, folder_name=''):
        filer_image = self._get_or_create_image(
                                        iif_obj.get_standard_resolution_url(),
                                        folder_name,
        )
        data = dict(instagram_id=iif_obj.id,
                    link=iif_obj.link,
                    data=iif_obj,
                    img=filer_image)
        iif, _crt = self.get_or_create(**data)
        return iif