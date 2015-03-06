#coding: utf-8
from __future__ import print_function, unicode_literals

__author__='smirnov.ev'

import datetime
import re
import requests

from django.db.models.loading import get_model

from . import GrabParser
from . import xpathes


KHL_PLAYER_RU_TO_EN = {
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
        'citizenship': b'Гражданство',
}


class GetAllKHLPlayerIDs(GrabParser):
    b''' Парсер списка игроков КХЛ '''
    url = xpathes.KHL_PLAYER_URL
    absolute_url = url
    as_get_param = True
    pk_kwarg = 'letter'
    player_xpath = '//td/div/a/@href'

    def _get_absolute_url(self, id=None, slash=True):
        b'''определяем url страницы
            По-умолчанию: self.absolute_url = self.url
        '''
        if id:
            if self.as_get_param:
                _url = b'?{0}={1}'.format(self.pk_kwarg,id.encode('utf-8'))
            else:
                _url = b'{0}{1}'.format(id,'/' if slash else '')
            self.absolute_url = b'{0}{1}'.format(self.url,_url)
        return self.absolute_url

    def get_page(self, id=None):
        b'''  смотрим список игроков '''
        self.page_tree = super(GetAllKHLPlayerIDs, self).get_page(id)
        if self.page_tree is not None:
            return self.page_tree.xpath(self.player_xpath)

    def get_ids(self):
        ids = list()
        for char in 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ':
            lst_link = self.get_page(id=char)
            ids.extend([elem.split('/')[2] for elem in lst_link])
        return set(ids)


class KHLPlayerInfo(GrabParser):
    b''' парсер данных о игроке КХЛ '''
    url = xpathes.KHL_PLAYER_URL
    absolute_url = url
    as_get_param = False
    body_xpath = xpathes.KHL_PLAYER_XPATH
    xpath_dict = xpathes.KHL_PLAYER_DATA_DICT
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
        self.page_tree = super(KHLPlayerInfo, self).get_page(id)
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
                    'fio': self.get_ru_fio(),
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

    def _get_dynamic_table_value_xpath(self,key,proxydict=KHL_PLAYER_RU_TO_EN):
        b''' динамически изменяем xpath '''
        i = self.stats_indexes.get(proxydict.get(key))
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
                return xpathes.KHL_SITE_URL+_res

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
        }.get(_res[0].strip().lower().encode('utf-8')) if _res else ''

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
            _res = _res.replace(_m, xpathes.MDP.get(_m).encode('utf-8'))
            return datetime.datetime.strptime(_res, '%d %m %Y')
        return ''

    def get_death_date(self):
        b''' возьмем дату смерти игрока '''
        _res = self._get_dynamic_table_value('death_date')        
        if _res:
            _res = _res[0].strip().lower().encode('utf-8')
            _m = _res.split()[1]
            _res = _res.replace(_m, xpathes.MDP.get(_m).encode('utf-8'))
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
################################################################################
################################################################################
################################################################################


MHL_PLAYER_RU_TO_EN = {
        'number': b'Номер',
        'line': b'Амплуа',
        'height': b'Рост',
        'weight': b'Вес',
        'birth_date': b'Дата рожд.',
        'citizenship': b'Гражданство',
}

class GetAllMHLPlayerIDs(GetAllKHLPlayerIDs):
    b''' Парсер списка игроков МХЛ '''
    url = xpathes.MHL_PLAYER_URL
    absolute_url = url
    player_xpath = '//td[@class="player_surname"]/a/@href'


class MHLPlayerInfo(KHLPlayerInfo):
    b''' парсер данных о игроке МХЛ '''
    url = xpathes.MHL_PLAYER_URL
    absolute_url = url
    body_xpath = xpathes.MHL_PLAYER_XPATH
    xpath_dict = xpathes.MHL_PLAYER_DATA_DICT
    stats_indexes =  {
                        b'Номер': -1,
                        b'Амплуа': -1,
                        b'Рост': -1,
                        b'Вес': -1,
                        b'Дата рожд.': -1,
                        b'Гражданство': -1,
    }

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
                    'fio': self.get_ru_fio(),
                    'ava_url': self.get_photo_url(),
                    'number': self.get_number(),
                    'line': self.get_line(),
                    'height': self.get_height(),
                    'weight': self.get_weight(),
                    'birth_date': self.get_birth_date(),
                    'citizenship': self.get_citizenship(),
            }
            _res['wiki_page'] = self.get_wiki_page(_res['fio'])
            self.clear_stats_indexes()
            return _res

    def _get_dynamic_table_value_xpath(self,key,proxydict=MHL_PLAYER_RU_TO_EN):
        b''' динамически изменяем xpath '''
        return super(MHLPlayerInfo, self)._get_dynamic_table_value_xpath(
                                            key,
                                            proxydict
        )

    def get_photo_url(self):
        b''' возьмем url photo игрока '''
        _res = self._get_value('photo')
        if _res:
            if ('/img/teamplayers_db//.jpg' not in _res[0] or 
                '/i/no_photo.gif' not in _res[0]
            ):
                return _res[0]

    def get_birth_date(self):
        b''' возьмем день рождения игрока '''
        _res = self._get_dynamic_table_value('birth_date')
        if _res:
            _res = _res[0].strip().lower().encode('utf-8')
            return datetime.datetime.strptime(_res, '%d.%m.%Y')
        return ''
################################################################################
################################################################################
################################################################################


class GetAllMHL2PlayerIDs(GetAllMHLPlayerIDs):
    b''' Парсер списка игроков МХЛ-2 '''
    url = xpathes.MHL2_PLAYER_URL
    absolute_url = url

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

    def get_ids(self):
        ids = list()
        for char in range(1,28):
            lst_link = self.get_page(id=char)
            ids.extend([elem.split('/')[2] for elem in lst_link])
        return set(ids)


MHL2_PLAYER_RU_TO_EN = {
        'club': b'Клуб',
        'number': b'Номер',
        'line': b'Амплуа',
        'height': b'Рост',
        'weight': b'Вес',
        'birth_date': b'Дата рожд.',
        'citizenship': b'Гражданство',
}

class MHL2PlayerInfo(MHLPlayerInfo):
    b''' парсер данных о игроке МХЛ-2 '''
    url = xpathes.MHL2_PLAYER_URL
    absolute_url = url
    body_xpath = xpathes.MHL2_PLAYER_XPATH
    xpath_dict = xpathes.MHL2_PLAYER_DATA_DICT
    stats_indexes =  {
                        b'Клуб': -1,
                        b'Номер': -1,
                        b'Амплуа': -1,
                        b'Рост': -1,
                        b'Вес': -1,
                        b'Дата рожд.': -1,
                        b'Гражданство': -1,
    }

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
                    'fio': self.get_ru_fio(),
                    'ava_url': self.get_photo_url(),
                    'club': self.get_club(),
                    'number': self.get_number(),
                    'line': self.get_line(),
                    'height': self.get_height(),
                    'weight': self.get_weight(),
                    'birth_date': self.get_birth_date(),
                    'citizenship': self.get_citizenship(),
            }
            _res['wiki_page'] = self.get_wiki_page(_res['fio'])
            self.clear_stats_indexes()
            return _res

    def _get_dynamic_table_value_xpath(self,key,proxydict=MHL2_PLAYER_RU_TO_EN):
        b''' динамически изменяем xpath '''
        return super(MHL2PlayerInfo, self)._get_dynamic_table_value_xpath(
                                            key,
                                            proxydict
        )
################################################################################
################################################################################
################################################################################


class GetAllVHLPlayerIDs(GetAllMHLPlayerIDs):
    b''' Парсер списка игроков ВХЛ '''
    url = xpathes.VHL_PLAYER_URL
    absolute_url = url
    player_xpath = '//td[@width="200"]/a/@href'


class VHLPlayerInfo(MHL2PlayerInfo):
    b''' парсер данных о игроке ВХЛ '''
    url = xpathes.VHL_PLAYER_URL
    absolute_url = url
    body_xpath = xpathes.VHL_PLAYER_XPATH
    xpath_dict = xpathes.VHL_PLAYER_DATA_DICT

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
                    'fio': self.get_ru_fio(),
                    'ava_url': self.get_photo_url(),
                    'club': self.get_club(),
                    'number': self.get_number(),
                    'line': self.get_line(),
                    'height': self.get_height(),
                    'weight': self.get_weight(),
                    'birth_date': self.get_birth_date(),
                    'citizenship': self.get_citizenship(),
            }
            _res['wiki_page'] = self.get_wiki_page(_res['fio'])
            self.clear_stats_indexes()
            return _res
################################################################################
################################################################################
################################################################################


class RhockeyPlayerInfoParser(GrabParser):
    b''' парсер данных о игроке с сайта http://r-hockey.ru/ '''
    url = 'http://r-hockey.ru/player.asp'
    absolute_url = url
    as_get_param = True
    pk_kwarg = 'TXT'
    body_xpath = 'body'
    xpath_dict = {
                    'fio': '/span[@id="Player"]/@value',
                    'birth_date': '/table/tr/td/table/tr/td/h3/text()',
                    'birth_place': '/table/tr/td/table/tr/td/h3/text()',
                    'first_school': '/table/tr/td/table/tr/td/h3/text()',
    }
    model_name = 'Player'

    def update_player(self, other_site_id):
        data = self.get_page(other_site_id)
        if data:
            model = get_model('hockeyapp', self.model_name)
            fio = data.pop('fio', None)
            if fio:
                plrs = model.objects.filter(fio=fio,
                                            birth_date__isnull=True)
                if not plrs.exists():
                    plrs = model.objects.filter(fio=fio)
                    data.pop('birth_date', None)
                if plrs.exists():
                    plrs.update(**data)

    def get_page(self, id=None):
        b'''  смотрим протокол матча '''
        self.page_tree = super(RhockeyPlayerInfoParser, self).get_page(id)
        if self.page_tree is not None:
            return self.get_player_all_data()

    def get_player_all_data(self):
        b'''
            Забираем данные o игроке через DOM-дерево
        '''
        if self.page_tree is not None:
            _res = {
                    'fio': self.get_fio(),
                    'birth_date': self.get_birth_date(),
                    'birth_place': self.get_birth_place(),
                    'first_school': self.get_first_school(),
            }
            return _res

    def get_fio(self):
        b''' возьмем ФИО игрока '''
        _res = self._get_value('fio')
        return _res[0].strip() if _res else ''

    def get_birth_date(self):
        b''' возьмем дату рождения игрока '''
        _res = self._get_value('birth_date')
        if _res:
            _res = _res[0].strip().split()
            if len(_res) > 1:
                _res = _res[1].strip('.')
                if _res:
                    return datetime.datetime.strptime(_res, '%d.%m.%Y')
        return ''

    def get_birth_place(self):
        b''' возьмем место рождения игрока '''
        _res = self._get_value('birth_place')
        if _res:
            _res = _res[0].strip().split()
            if len(_res) > 2 and _res[2][0] == '(':
                return _res[2][1:-2]
        return ''

    def get_first_school(self):
        b''' возьмем первую школу игрока '''
        _res = self._get_value('first_school')
        if _res:
            _res = _res[0].strip().split('-')
            if len(_res) > 1:
                if _res[1].strip() != '?':
                    return _res[1].strip()
        return ''