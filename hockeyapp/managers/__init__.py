#coding: utf-8
__author__='smirnov.ev'

import requests

from StringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile

import filer


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


from . import arena, club, match, player