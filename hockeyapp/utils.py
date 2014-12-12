#coding: utf-8
from __future__ import print_function
import grab

from django.db.models.loading import get_model

#from django.conf import settings
from .defaults import DEFAULT_KHL_MATCH_PROTOCOL_XPATH, DEFAULT_BODY_NOTEXISTS
from .defaults import DEFAULT_EMPTY_PAGE_TEXT, DEFAULT_BODY_XPATH, DEFAULT_URL
from .defaults import DEFAULT_MATCH_REPORT_DICT
from .defaults import DEFAULT_PLAYER_URL, DEFAULT_PLAYER_XPATH
from .defaults import DEFAULT_PLAYER_DATA_DICT


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

    def _get_value(self, key):
        b''' универсальный метод получение значения из DOM через xpath '''
        return self.page_tree.xpath(self._get_value_xpath(key))

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


class GetPlayerInfo(GrabParser):
    url = DEFAULT_PLAYER_URL
    absolute_url = url
    as_get_param = False
    body_xpath = DEFAULT_PLAYER_XPATH
    xpath_dict = DEFAULT_PLAYER_DATA_DICT
    model_name = 'Player'

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
            return {
                    'khl_id': khl_id,
                    #'html_body': html_body or '',
                    'ru_fio': self.get_ru_fio(),
                    'en_fio': self.get_en_fio(),
                    'line': self.get_line(),
            }

    def get_ru_fio(self):
        b''' возьмем значение даты матча '''
        _res = self._get_value('ru_fio')
        return _res[0].strip() if _res else ''

    def get_en_fio(self):
        b''' возьмем значение даты матча '''
        _res = self._get_value('en_fio')
        return _res[0].strip() if _res else ''

    def get_line(self):
        b''' возьмем значение даты матча '''
        _res = self._get_value('line')
        return {
                '': 0,
                b'вратарь': 1,
                b'защитник': 2,
                b'нападающий': 3,
        }.get(_res[0].strip().encode('utf-8')) if _res else ''


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
            body = self.page_tree.xpath(self.match_protocol_xpath)[0]
            if body.text_content().find(DEFAULT_EMPTY_PAGE_TEXT) == -1:
                #протокол игры существует
                body = self.page_tree.xpath(self.body_xpath)[0]
                body = body.text_content().encode('utf-8')
                if body.find(DEFAULT_BODY_NOTEXISTS) == -1:
                    #протокол найден, собираем данные
                    _html_body = self.g.response.unicode_body()
                    return self.get_match_all_data(id, html_body=_html_body)

    def get_match_all_data(self, matchid=None, html_body=None):
        b''' метод запускается, в случае если протокол игры существует и найден
            Забираем данные из протокола игры через DOM-дерево
        '''
        if self.page_tree is not None:
            _home_coach = self.get_home_team_coach()
            _guest_coach = self.get_guest_team_coach()
            _home_players = self.get_home_players()
            _guest_players = self.get_guest_players()
            return {
                    'khl_id': matchid,
                    'html_body': html_body or '',
                    'url': self.absolute_url,
                    'ru_title': self.get_match_num(),
                    'spectators': self.get_spectators(),
                    'date': self.get_match_date(),
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
                    'penalties_history': self.get_penalties_history()
            }

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
        res = {
                'time': tr.xpath('td[@class="time"]/strong')[0].text,
                'duration': _dur.strip(),
                'player': tr.xpath('td/a')[0].attrib.get('href',''
                                            ).split('/')[-2],
                'ptype': _ptype.strip(),
        }
        return res

    def get_home_players(self):
        b''' получаем игроков домашней команды '''
        res = list()
        res.extend(self._get_players('home_keepers', 1))
        res.extend(self._get_players('home_defenders', 2))
        res.extend(self._get_players('home_offenders', 3))
        return res

    def get_guest_players(self):
        b''' получаем игроков гостевой команды '''
        res = list()
        res.extend(self._get_players('guest_keepers', 1))
        res.extend(self._get_players('guest_defenders', 2))
        res.extend(self._get_players('guest_offenders', 3))
        return res

    def get_goals_history(self):
        b''' заброшенные шайбы '''
        goals_table = self._get_value('goals_history')[0]
        return [self._get_goal_data(tr) for tr in goals_table.xpath('tr')
                if tr.attrib.get('class', '') != 'header']

    def _get_goal_data(self, tr):
        b''' данные о заброшенной шайбе '''
        _parity = _PARITTYDICT.get( tr.xpath('td[5]')[0].text.strip(
                                                            ).encode('utf-8'),
                                    0)
        res = {
                'period': tr.xpath('td[2]')[0].text_content().strip(),
                'time': tr.xpath('td[3]')[0].text.strip(),
                'parity': _parity,
                'scorer': tr.xpath('td[6]/a')[0].attrib.get('href',''
                                            ).split('/')[-2],
                'assist': self._get_assist(tr),
                'home_five_numbers': tr.xpath('td[9]')[0].text.strip(),
                'home_five_numbers': tr.xpath('td[10]')[0].text.strip(),
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
        raw_link = tr.cssselect('td.empty_bg')[1]
        khl_id = raw_link.cssselect('a')[0].attrib['href'].split('/')[-2]
        res = {
                'number': tr.cssselect('td.empty_bg > strong')[0].text,
                'khl_id': khl_id,
                'line': tp    
        }
        return res

    def _get_players(self, key, tp):
        b''' получаем игроков команды '''
        plrs_table = self._get_value(key)[0]
        return (self._get_player_data(tr, tp) for tr in plrs_table.xpath('tr')
                if tr.attrib.get('class', '') != 'header')

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