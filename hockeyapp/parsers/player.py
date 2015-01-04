#coding: utf-8
from __future__ import print_function, unicode_literals

__author__='smirnov.ev'

import datetime
import re
import requests

from .. import defaults

from . import GrabParser


PLAYER_RU_TO_EN = {
        'club': b'Клуб',
        'contract_type': b'Вид контракта',
        'contract_to': b'Контракт до',
        'number': b'Номер',
        'line': b'Амплуа',
        'height': b'Рост',
        'weight': b'Вес',
        'grip': b'Хват',
        'birth_date': b'Дата рождения',
        'birth_date_alt': b'Родился',
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
                        b'Клуб': -1,
                        b'Вид контракта': -1,
                        b'Контракт до': -1,
                        b'Номер': -1,
                        b'Амплуа': -1,
                        b'Рост': -1,
                        b'Вес': -1,
                        b'Хват': -1,
                        b'Дата рождения': -1,
                        b'Родился': -1,
                        b'Умер': -1,
                        b'Гражданство': -1,
    }

    def get_page(self, id=None):
        b'''  смотрим протокол матча '''
        self.page_tree = super(GetPlayerInfo, self).get_page(id)
        if self.page_tree is not None:
            _html_body = self.g.response.unicode_body()
            return self.get_player_all_data(id, html_body=_html_body)

    def get_player_all_data(self, khl_id=None, html_body=None):
        b'''
            Забираем данные o игроке через DOM-дерево
        '''
        if self.page_tree is not None:
            self.update_stats_indexes()
            _res = {
                    'khl_id': khl_id,
                    'url': self.absolute_url,
                    'html_body': self.get_html_body(html_body),
                    'ru_fio': self.get_ru_fio(),
                    'en_fio': self.get_en_fio(),
                    'ava_url': self.get_photo_url(),
                    'club': self.get_club(),
                    'contract_type': self.get_contract_type(),
                    'contract_to': self.get_contract_to(),
                    'number': self.get_number(),
                    'line': self.get_line(),
                    'height': self.get_height(),
                    'weight': self.get_weight(),
                    'grip': self.get_grip(),
                    'birth_date': self.get_birth_date(),
                    'death_date': self.get_death_date(),
                    'citizenship': self.get_citizenship(),
            }
            _res['wiki_page'] = self.get_wiki_page(_res['ru_fio'])
            self.clear_stats_indexes()
            return _res

    def clear_stats_indexes(self):
        for k in self.stats_indexes.keys():
            self.stats_indexes[k] = -1

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

    def _get_dynamic_table_value(self, key):
        b''' берем значеиние по динамической таблице '''
        _xpath = self._get_dynamic_table_value_xpath(key)
        return self._get_value(key, _xpath)

    def get_photo_url(self):
        b''' возьмем url photo игрока '''
        _res = self._get_value('photo')
        if _res:
            _res = _res[0].attrib.get('style')
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

    def get_club(self):
        b''' возьмем клуб игрока '''
        _res = self._get_dynamic_table_value('club')
        return _res[0].strip() if _res else ''

    def get_contract_type(self):
        b''' возьмем тип контракта игрока '''
        _res = self._get_dynamic_table_value('contract_type')
        return _res[0].strip() if _res else ''

    def get_contract_to(self):
        b''' возьмем дату окончания контракта игрока '''
        _res = self._get_dynamic_table_value('contract_to')
        if _res:
            _res = _res[0].strip().lower().encode('utf-8')
            return datetime.datetime.strptime(_res, '%d.%m.%Y')
        return ''

    def get_number(self):
        b''' возьмем номер игрока '''
        _res = self._get_dynamic_table_value('number')
        return _res[0].strip() if _res else ''

    def get_line(self):
        b''' возьмем амплуа игрока '''
        _res = self._get_dynamic_table_value('line')
        return {
                '': 0,
                b'вратарь': 1,
                b'защитник': 2,
                b'нападающий': 3,
        }.get(_res[0].strip().encode('utf-8')) if _res else ''

    def get_height(self):
        b''' возьмем рост игрока '''
        _res = self._get_dynamic_table_value('height')
        return _res[0].strip() if _res else ''

    def get_weight(self):
        b''' возьмем вес игрока '''
        _res = self._get_dynamic_table_value('weight')
        return _res[0].strip() if _res else ''

    def get_grip(self):
        b''' возьмем хват игрока '''
        _res = self._get_dynamic_table_value('grip')
        if _res:
            return _res[0].strip()
        else:
            _res = self._get_dynamic_table_value('all')
            if _res:
                return _res[0].strip()
        return ''

    def get_birth_date(self):
        b''' возьмем день рождения игрока '''
        _res = (self._get_dynamic_table_value('birth_date') or
                self._get_dynamic_table_value('birth_date_alt'))          
        if _res:
            _res = _res[0].strip().lower().encode('utf-8')
            _m = _res.split()[1]
            _res = _res.replace(_m, defaults.MDP.get(_m).encode('utf-8'))
            return datetime.datetime.strptime(_res, '%d %m %Y')
        return ''

    def get_death_date(self):
        b''' возьмем дату смерти игрока '''
        _res = self._get_dynamic_table_value('death_date')        
        if _res:
            _res = _res[0].strip().lower().encode('utf-8')
            _m = _res.split()[1]
            _res = _res.replace(_m, defaults.MDP.get(_m).encode('utf-8'))
            return datetime.datetime.strptime(_res, '%d %m %Y')
        return ''

    def get_citizenship(self):
        b''' возьмем хват игрока '''
        _res = self._get_dynamic_table_value('citizenship')
        if _res:
            return _res[0].strip()
        else:
            _res = self._get_dynamic_table_value('all')
            if len(_res) > 1:
                return _res[1].strip()
        return ''

    def get_wiki_page(self, ru_fio):
        b''' URL страницы на wiki '''
        if ru_fio:
            url = 'https://ru.wikipedia.org/w/api.php?action=opensearch&format=json&search='
            url = '{}{}'.format(url,ru_fio)
            r = requests.get(url)
            if r.status_code == 200 and r.json():
                if len(r.json()) > 3:
                    try:
                        return r.json()[3][0]
                    except:
                        pass
        return ''