#coding: utf-8
from __future__ import print_function, unicode_literals

__author__='smirnov.ev'

import datetime
import re

from .. import defaults

from . import GrabParser


PLAYER_RU_TO_EN = {
        'club': b'Клуб',
        'contract_type': b'Вид контракта',
        'contract_date_end': b'Контракт до',
        'number': b'Номер',
        'line': b'Амплуа',
        'height': b'Рост',
        'weight': b'Вес',
        'grip': b'Хват',
        'birth_date': b'Дата рождения',
}


class GetAllPlayerIDs(GrabParser):
    url = defaults.PLAYER_URL
    absolute_url = url
    as_get_param = True
    pk_kwarg = 'letter'

    def get_page(self, id=None):
        b'''  смотрим список игроков '''
        self.page_tree = super(GetAllPlayerIDs, self).get_page(id)
        if self.page_tree is not None:
            return self.page_tree.xpath('//td/div/a/@href')


class GetPlayerInfo(GrabParser):
    url = defaults.PLAYER_URL
    absolute_url = url
    as_get_param = False
    body_xpath = defaults.PLAYER_XPATH
    xpath_dict = defaults.PLAYER_DATA_DICT
    model_name = 'Player'
    stats_indexes =  {
                        b'Клуб': 1,
                        b'Вид контракта': 2,
                        b'Контракт до': 3,
                        b'Номер': 4,
                        b'Амплуа': 5,
                        b'Рост': 6,
                        b'Вес': 7,
                        b'Хват': 8,
                        b'Дата рождения': 9,
    }

    def get_page(self, id=None):
        b'''  смотрим протокол матча '''
        self.page_tree = super(GetPlayerInfo, self).get_page(id)
        if self.page_tree is not None:
            #_html_body = self.g.response.unicode_body()
            return self.get_player_all_data(id)#, html_body=_html_body)

    def get_player_all_data(self, khl_id=None, html_body=None):
        b'''
            Забираем данные o игроке через DOM-дерево
        '''
        if self.page_tree is not None:
            self.update_stats_indexes()
            return {
                    'khl_id': khl_id,
                    'html_body': self.get_html_body(html_body),
                    'ru_fio': self.get_ru_fio(),
                    'en_fio': self.get_en_fio(),
                    'ava_url': self.get_photo_url(),
                    'line': self.get_line(),
                    'birth_date': self.get_birth_date(),
                    'weight': self.get_weight(),
                    'height': self.get_height(),
                    #'grip': self.get_grip(),
            }

    def update_stats_indexes(self):
        b'''берем индексы данных игрока динамически,
            так как таблица изменяема от игрока к игроку
        '''
        table = self._get_value('stats')
        for li in table:
            key = li.text.split(':', 1)[0].encode('utf-8')
            if self.stats_indexes.get(key):
                self.stats_indexes[key] = table.index(li)+1

    def _get_dynamic_table_value_xpath(self, key):
        b''' динамически изменяем xpath '''
        i = self.stats_indexes.get(PLAYER_RU_TO_EN.get(key))
        _xpath = self._get_value_xpath(key)
        _repl = 'ul/li[{}]/b/'.format(i,)
        return re.sub('ul/li\[\d+\]/b/', _repl, _xpath)

    def get_photo_url(self):
        b''' возьмем url photo игрока '''
        _res = self._get_value('photo')[0].attrib.get('style')
        _res = re.search('url\((.*?)\)', _res).group(1)
        if _res != '/img/teamplayers_db//.jpg':
            return defaults.KHL_SITE_URL+_res

    def get_ru_fio(self):
        b''' возьмем ФИО игрока '''
        _res = self._get_value('ru_fio')
        return _res[0].strip() if _res else ''

    def get_en_fio(self):
        b''' возьмем Full name игрока '''
        _res = self._get_value('en_fio')
        return _res[0].strip() if _res else ''

    def get_line(self):
        b''' возьмем амплуа игрока '''
        _key = 'line'
        _xpath = self._get_dynamic_table_value_xpath(_key)
        _res = self._get_value(_key, _xpath)
        return {
                '': 0,
                b'вратарь': 1,
                b'защитник': 2,
                b'нападающий': 3,
        }.get(_res[0].strip().encode('utf-8')) if _res else ''

    def get_birth_date(self):
        b''' возьмем день рождения игрока '''
        _key = 'birth_date'
        _xpath = self._get_dynamic_table_value_xpath(_key)
        _res = self._get_value(_key, _xpath)
        if _res:
            _res = _res[0].strip().lower().encode('utf-8')
            _m = _res.split()[1]
            _res = _res.replace(_m, defaults.MDP.get(_m).encode('utf-8'))
            return datetime.datetime.strptime(_res, '%d %m %Y')
        return ''

    def get_weight(self):
        b''' возьмем вес игрока '''
        _key = 'weight'
        _xpath = self._get_dynamic_table_value_xpath(_key)
        _res = self._get_value(_key, _xpath)
        return _res[0].strip() if _res else ''

    def get_height(self):
        b''' возьмем рост игрока '''
        _key = 'height'
        _xpath = self._get_dynamic_table_value_xpath(_key)
        _res = self._get_value(_key, _xpath)
        return _res[0].strip() if _res else ''

    def get_grip(self):
        b''' возьмем рост игрока '''
        _key = 'grip'
        _xpath = self._get_dynamic_table_value_xpath(_key)
        _res = self._get_value(_key, _xpath)
        return _res[0].strip() if _res else ''