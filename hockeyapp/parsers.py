#coding: utf-8
from __future__ import print_function
import datetime
import grab
import re
import time

from django.db.models.loading import get_model

#from django.conf import settings
from .defaults import DEFAULT_KHL_MATCH_PROTOCOL_XPATH, DEFAULT_BODY_NOTEXISTS
from .defaults import DEFAULT_EMPTY_PAGE_TEXT, DEFAULT_BODY_XPATH, DEFAULT_URL
from .defaults import DEFAULT_MATCH_REPORT_DICT, MD, MDP
from .defaults import DEFAULT_PLAYER_URL, DEFAULT_PLAYER_XPATH
from .defaults import DEFAULT_PLAYER_DATA_DICT, DEFAULT_SITE_URL


class GrabParser(object):
    url = None
    absolute_url = url
    pk_kwarg = 'id'
    as_get_param = True
    page_tree = None
    model_name = None

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

    def get_page(self, id=None):
        b'''  берем DOM страницы  '''
        id = self.url and self.pk_kwarg and id
        if id:
            if self.as_get_param:
                self.absolute_url = '{0}?{1}={2}'.format(   self.url,
                                                            self.pk_kwarg,
                                                            id)
            else:
                self.absolute_url = '{0}{1}/'.format( self.url,id)
            self.g = grab.Grab(url=self.absolute_url)
            # забираем ответ от ресурса
            try:
                self.g.go(self.absolute_url)
            except grab.error.GrabNetworkError: 
                self.g = None
            if self.g and self.g.response.code == 200:
                # страница доступна
                self.page_tree = self.g.tree
                return self.page_tree

    def put_data_in_db_from_page(self, id=None):
        b'''Основной метод, берующий данные со стороннего сайта и кладущий
            в БД, если все хорошо
        ''' 
        data = self.get_page(id)
        if data and self.model_name:
            model = get_model('hockeyapp', self.model_name)
            return model.objects.get_or_create(**data)


class GetAllPlayerIDs(GrabParser):
    url = DEFAULT_PLAYER_URL
    absolute_url = url
    as_get_param = True
    pk_kwarg = 'letter'

    def get_page(self, id=None):
        b'''  смотрим список игроков '''
        self.page_tree = super(GetAllPlayerIDs, self).get_page(id)
        if self.page_tree is not None:
            return self.page_tree.xpath('//td/div/a/@href')


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


class GetPlayerInfo(GrabParser):
    url = DEFAULT_PLAYER_URL
    absolute_url = url
    as_get_param = False
    body_xpath = DEFAULT_PLAYER_XPATH
    xpath_dict = DEFAULT_PLAYER_DATA_DICT
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
                    #'html_body': html_body or '',
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
            return DEFAULT_SITE_URL+_res

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
            _res = _res.replace(_m, MDP.get(_m).encode('utf-8'))
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


_PARITTYDICT = {
            b'рав.': 1,
            b'бол.': 2,
            b'мен.': 3,
            b'бул.': 4,
            b'': 0,
        }


class HockeyMatchParser(GrabParser):
    b'''Парсер хоккейной статистики матча'''
    url = DEFAULT_URL
    absolute_url = url
    pk_kwarg = 'idgame'
    as_get_param = True
    match_protocol_xpath = DEFAULT_KHL_MATCH_PROTOCOL_XPATH
    page_tree = None
    body_xpath = DEFAULT_BODY_XPATH
    xpath_dict = DEFAULT_MATCH_REPORT_DICT
    model_name = 'Match'

    def put_data_in_db_from_page(self, id=None):
        b'''Основной метод, берующий данные со стороннего сайта и кладущий
            в БД, если все хорошо
        ''' 
        data = self.get_page(id)
        if data and self.model_name:
            model = get_model('hockeyapp', self.model_name)
            return model.objects.get_or_create_match(**data)

    def get_page(self, id=None):
        b'''  смотрим протокол матча '''
        self.page_tree = super(HockeyMatchParser, self).get_page(id)
        if self.page_tree is not None:
            if self.page_tree.xpath(self.match_protocol_xpath):
                body = self.page_tree.xpath(self.match_protocol_xpath)[0]
                if body.text_content().find(DEFAULT_EMPTY_PAGE_TEXT) == -1:
                    #протокол игры существует
                    body = self.page_tree.xpath(self.body_xpath)[0]
                    body = body.text_content().encode('utf-8')
                    if body.find(DEFAULT_BODY_NOTEXISTS) == -1:
                        #протокол найден, собираем данные
                        _html_body = self.g.response.unicode_body()
                        return self.get_match_all_data(id, html_body=_html_body)
            else:
                time.sleep(60)
                self.get_page(id)

    def get_match_all_data(self, matchid=None, html_body=None):
        b''' метод запускается, в случае если протокол игры существует и найден
            Забираем данные из протокола игры через DOM-дерево
        '''
        if self.page_tree is not None:
            _home_coach = self.get_home_team_coach()
            _guest_coach = self.get_guest_team_coach()
            _home_players = self.get_home_players()
            _guest_players = self.get_guest_players()
            _date = self.get_match_date()
            return {
                    'khl_id': matchid,
                    'html_body': html_body or '',
                    'url': self.absolute_url,
                    'ru_title': self.get_match_num(),
                    'spectators': self.get_spectators(),
                    'date': _date,
                    'count': self.get_match_count(),
                    'detail_count': self.get_match_detail_count(),
                    'judges': self.get_match_judges(),
                    'line_judges': self.get_match_line_judges(),
                    'home_team': {
                                    'ru_title': self.get_home_team(),
                                    'region':  self.get_home_team_region(),
                                    'coach': _home_coach,
                                    'players': _home_players,
                                },
                    'home_coach': _home_coach,
                    'home_players': _home_players,
                    'guest_team': {
                                    'ru_title': self.get_guest_team(),
                                    'region':  self.get_guest_team_region(),
                                    'coach': _guest_coach,
                                    'players': _guest_players,
                                },
                    'guest_coach': _guest_coach,
                    'guest_players': _guest_players,
                    'goals_history': self.get_goals_history(),
                    'penalties_history': self.get_penalties_history(),
                    'season': { 
                                'start_date':self.start_date(_date),
                                'end_date': self.end_date(_date),
                    }
            }

    def python_date(self, date):
        b''' парсит дату в datetime object '''
        if date:
            _date_dict = date.strip().lower().split(',')
            _dt = _date_dict[:2]
            _dt.append(_date_dict[3])
            _date_dict = _dt
            _m = _date_dict[0].split()[1].encode('utf-8')
            _date_dict[0] = _date_dict[0].replace(_m.decode('utf-8'), MD.get(_m))
            if _date_dict[-1] != '':
                mask = '%d %m %Y %H:%M'
            else:
                mask = '%d %m %Y'
            _dt = ''.join(_date_dict).encode('utf-8')
            return datetime.datetime.strptime(_dt, mask)

    def start_date(self, date):
        b''' возвращает дату начала сезона '''
        _pdt = self.python_date(date)
        _year = _pdt.year - 1 if _pdt.month < 7 else _pdt.year
        return datetime.datetime(day=1, month=7, year=_year)

    def end_date(self, date):
        b''' возвращает дату окончания сезона '''
        _pdt = self.python_date(date)
        _year = _pdt.year + 1 if _pdt.month > 6 else _pdt.year
        return datetime.datetime(day=30, month=6, year=_year)
        
    def get_penalties_history(self):
        b''' штрафы '''
        penalty_table = self._get_value('penalties_history')[0]
        return [self._get_penalty_data(tr) for tr in penalty_table.xpath('tr')
                if tr.attrib.get('class', '') not in (  'header', 
                                                        'report',
                                                        'first_row',
                                                    )
        ]

    def _get_penalty_data(self, tr):
        b''' данные о штрафе '''
        _tds = tr.xpath('td')
        _ptype = _tds[3].text if _tds[3].text else _tds[8].text
        _dur = _tds[2].text if _tds[2].text else _tds[7].text
        _time = self._get_value_or_blank(tr.xpath('td[@class="time"]/strong'))
        res = {
                'time': _time,
                'duration': _dur.strip(),
                'ptype': _ptype.strip(),
        }
        if tr.xpath('td/a'):
            _player = tr.xpath('td/a')[0].attrib.get('href','///'
                                                     ).split('/')[-2],
            if _player:
                res['player'] = isinstance(_player, tuple) and _player[0]

        return res

    def get_home_players(self):
        b''' получаем игроков домашней команды '''
        _crtg = (   ('home_keepers', 1),
                    ('home_defenders', 2),
                    ('home_offenders', 3),
        )
        return self._get_players_list(_crtg)

    def get_guest_players(self):
        b''' получаем игроков гостевой команды '''
        _crtg = (   ('guest_keepers', 1),
                    ('guest_defenders', 2),
                    ('guest_offenders', 3)
        )
        return self._get_players_list(_crtg)

    def _get_players_list(self, crtg):
        res = list()
        for k,v in crtg:
            _plrs = self._get_players(k,v)
            if _plrs:
                res.extend(_plrs)
        return res

    def get_goals_history(self):
        b''' заброшенные шайбы '''
        goals_table = self._get_value('goals_history')[0]
        return [self._get_goal_data(tr) for tr in goals_table.xpath('tr')
                if tr.attrib.get('class', '') != 'header']

    def _get_goal_data(self, tr):
        b''' данные о заброшенной шайбе '''
        _parity = _PARITTYDICT.get(
                    self._get_value_or_blank(tr.xpath('td[5]')).encode('utf-8'),
                    0
        )
        res = {
                'period': tr.xpath('td[2]')[0].text_content().strip(),
                'time': tr.xpath('td[3]')[0].text.strip(),
                'parity': _parity,
                'scorer': tr.xpath('td[6]/a')[0].attrib.get('href',''
                                            ).split('/')[-2],
                'assist': self._get_assist(tr),
                'home_five_numbers': self._get_value_or_blank(tr.xpath('td[9]')),
                'guest_five_numbers': self._get_value_or_blank(tr.xpath('td[10]')),
        }
        return res

    def _get_assist(self, tr):
        b''' ассистенты '''
        res = []
        if tr.xpath('td[7]/a'):
            res.append(tr.xpath('td[7]/a')[0].attrib.get('href').split('/')[-2])
        if tr.xpath('td[8]/a'):
            res.append(tr.xpath('td[8]/a')[0].attrib.get('href').split('/')[-2])
        return set(res)

    def _get_player_data(self, tr, tp):
        b''' берем значения номер, id и тип игрока '''
        _raw_link = tr.xpath('td[@class="empty_bg"]/a')
        if _raw_link:
            _raw_link = tr.xpath('td[@class="empty_bg"]/a')[0]
            res = {
                    'number': tr.xpath('td[@class="empty_bg"]/strong')[0].text,
                    'khl_id': _raw_link.attrib.get('href','').split('/')[-2],
                    'line': tp,
                    'ru_fio': _raw_link.text  
            }
            return res

    def _get_players(self, key, tp):
        b''' получаем игроков команды '''
        plrs_table = self._get_value(key)
        if plrs_table:
            #TODO: refact this
            return (self._get_player_data(tr, tp) for tr 
                    in plrs_table[0].xpath('tr')
                    if tr.attrib.get('class', '') != 'header'
                    and self._get_player_data(tr, tp))

    def get_match_num(self):
        b''' возьмем значение номера матча '''
        _res = self._get_value('match_num')
        return _res[0].text.split('.')[0] if _res else ''

    def get_match_date(self):
        b''' возьмем значение даты матча '''
        _res = self._get_value('match_date')
        return _res[0].text.split('.')[1] if _res else ''

    def get_spectators(self):
        b''' возьмем значение посещаемости '''
        _res = self._get_value('match_spectators')
        return _res[0].text.split(':')[1] if _res else ''

    def get_home_team(self):
        b''' получаем имя домашней команды '''
        _res = self._get_value('home_team')
        return _res[0].text.strip() if _res else ''

    def get_home_team_region(self):
        b''' получаем регион домашней команды '''
        _res = self._get_value('home_team_region')
        return _res[0].text[1:-1] if _res else ''

    def get_home_team_coach(self):
        b''' получаем тренера домашней команды '''
        _res = self._get_value('home_team_coach')
        return _res[0].strip() if _res else ''

    def get_guest_team(self):
        b''' получаем имя гостевой команды '''
        _res = self._get_value('guest_team')
        return _res[0].text.strip() if _res else ''

    def get_guest_team_region(self):
        b''' получаем регион гостевой команды '''
        _res = self._get_value('guest_team_region')
        return _res[0].text[1:-1] if _res else ''

    def get_guest_team_coach(self):
        b''' получаем тренера гостевой команды '''
        _res = self._get_value('guest_team_coach')
        return _res[0].strip() if _res else ''

    def get_match_count(self):
        b''' получаем счет матча '''
        _res = self._get_value('match_count')
        return _res[0].strip() if _res else ''

    def get_match_detail_count(self):
        b''' получаем детальный счет матча '''
        _res = self._get_value('match_detail_count')
        return _res[0].strip() if _res else ''

    def get_match_judges(self):
        b''' получаем судей матча '''
        _res = self._get_value('match_judges')
        if _res:
            _res = _res[0].text_content().strip().split('\n')
            return [j.strip() for j in _res[1:]]
        return ''

    def get_match_line_judges(self):
        b''' получаем линейных судей матча '''
        _res = self._get_value('match_line_judges')
        if _res:
            _res = _res[0].text_content().strip().split('\n')
            return [j.strip() for j in _res[1:]]
        return ''