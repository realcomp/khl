#coding: utf-8
from __future__ import print_function, unicode_literals

__author__='smirnov.ev'

import grab
import time

from lxml.html import fromstring

from django.db.models.loading import get_model


class GrabParser(object):
    url = None
    absolute_url = url
    pk_kwarg = 'id'
    as_get_param = True
    page_tree = None
    model_name = None
    html = True

    def __init__(self, html=None, absolute_url=None):
        super(GrabParser, self).__init__()
        self.html = html or self.html
        self.absolute_url = absolute_url or self.absolute_url
        if not self.url:
            self.url = self.absolute_url

    def put_data_in_db_from_page(self, id=None):
        b'''Основной метод, берующий данные со стороннего сайта и кладущий
            в БД, если все хорошо
        ''' 
        data = self.get_page(id)
        if data and self.model_name:
            model = get_model('hockeyapp', self.model_name)
            return model.objects.get_or_create(**data)

    def get_page_from_db(self, obj):
        b''' Парсинг html из ДБ '''
        if obj.html_body:
            html_body = obj.html_body
            self.page_tree = fromstring(html_body)
            return self.get_match_all_data(obj.khl_id, html_body, obj.url)

    def update_model_object(self, obj):
        b''' Обновляем данные '''
        data = self.get_page_from_db(obj)
        return self.put_data_in_db_from_page(obj.khl_id, data)

    def get_html_body(self, html_body=None):
        return html_body if self.html and html_body else ''

    def _get_value_xpath(self, key):
        b''' универсальный метод получение xpath до значения '''
        _xpath = self.body_xpath or ''
        _inherit_xpath_dict = self.xpath_dict or {}
        return _xpath+_inherit_xpath_dict.get(key, '')

    def _get_value(self, key, xpath=None):
        b''' универсальный метод получение значения из DOM через xpath '''
        if xpath:
            return self.page_tree.xpath(xpath)
        return self.page_tree.xpath(self._get_value_xpath(key))

    def _get_value_or_blank(self, xpath_val):
        b'''возвращает либо значение xpath-массива, либо blank '''
        if xpath_val and xpath_val[0].text:
            return xpath_val[0].text.strip()
        return ''

    def _get_strip_value(self, key):
        b'''возвращает первое значение xpath-string-массива, либо blank '''
        xpath_val = self._get_value(key)
        if xpath_val and xpath_val[0]:
            return xpath_val[0].strip()
        return ''

    def _get_absolute_url(self, id=None, slash=True):
        b'''определяем url страницы
            По-умолчанию: self.absolute_url = self.url
        '''
        if id:
            if self.as_get_param:
                _url = b'?{0}={1}'.format(self.pk_kwarg,id)
            else:
                _url = b'{0}{1}'.format(id,'/' if slash else '')
            self.absolute_url = b'{0}{1}'.format(self.url,_url)
        return self.absolute_url

    def get_page(self, id=None, slash=True, count=None):
        b'''  берем DOM страницы  '''
        if self.url and self.pk_kwarg:
            self._get_absolute_url(id, slash)
            self.g = grab.Grab(url=self.absolute_url)
            # забираем ответ от ресурса
            count = count or 0
            try:
                self.g.go(self.absolute_url)
            except grab.error.GrabNetworkError: 
                self.g = None
            except grab.error.GrabConnectionError:
                if count < 3:
                    count+=1
                    time.sleep(60)
                    return self.get_page(id, slash, count)
            if self.g and self.g.response.code == 200:
                # страница доступна
                self.page_tree = self.g.tree
                return self.page_tree

from . import player, match, club, schedule
