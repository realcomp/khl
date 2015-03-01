#coding: utf-8
from __future__ import print_function, unicode_literals

__author__='smirnov.ev'

import datetime
import json
import re
import time

from lxml.html import fromstring

from django.db.models.loading import get_model
from django.utils import timezone
current_tz = timezone.get_current_timezone()

from base.utils import str2int_safe, str2float_safe, str2sec_safe

from ..utils import khl_string_data2python_obj_safe

from . import GrabParser
from . import xpathes


_PARITTYDICT = {
            b'рав.': 1,
            b'бол.': 2,
            b'мен.': 3,
            b'бул.': 4,
            b'': 0,
        }


class AdvancedHockeyMatchParser(GrabParser):
    b''' Парсер дополнительной статистики матча из текстовой трансляции '''
    url = xpathes.MATCH_ADV_STATS_URL
    absolute_url = url
    as_get_param = False
    match_protocol_xpath = xpathes.MATCH_ADV_STATS_XPATH
    body_xpath = xpathes.MATCH_ADV_STATS_XPATH
    xpath_dict = xpathes.MATCH_ADV_STATC_DICT
    teams = None

    def get_page(self, id=None):
        b'''  смотрим протокол матча '''
        if id:
            id = '{0}.{1}'.format(id,'html')
        self.page_tree=super(AdvancedHockeyMatchParser, self).get_page(id,False)
        if self.page_tree is not None:
            if self.page_tree.xpath(self.match_protocol_xpath):
                _html_body = self.g.response.unicode_body()
                return self.get_adv_stats(_html_body)

    def get_adv_stats(self, html_body=None):
        b''' Словарь статистики команд '''
        res = {
                'hp': self._get_team_players(self.xpath_dict['home_team']),
                'gp': self._get_team_players(self.xpath_dict['guest_team']),
                #'html_body': self.get_html_body(html_body),
        }
        self._get_player_fivers(res)
        return res

    def _get_team_players(self, xpath_dict):
        b''' Словарь статистики команды '''
        res = self._get_extra_stats(xpath_dict['shots'], 
                                    xpathes.MATCH_PLAYER_SHOTS,
                                    text_content=True,
                                    table_name = 'shots',
        )
        for key,_xpathes in (
                            ('faceoff',xpathes.MATCH_PLAYER_FACEOFFS,),
                            ('gamingtime', xpathes.MATCH_PLAYER_GAMINGTIMES),
                            ('extra', xpathes.MATCH_PLAYER_EXTRAS),

        ):
            self._get_extra_stats(  
                                xpath_dict[key],
                                _xpathes,
                                res,
                                table_name=key
            )
        return res

    def _get_player_number(self, val):
        b''' Номер игрока '''
        _res = re.findall(r'\d+', val)
        return _res[0] if _res else None

    def _get_extra_stats(self, xpath, xpath_dict, res=None, text_content=False,
                        table_name=''):
        b''' Универсальный метод получения статистики из таблиц '''
        trs = self.page_tree.xpath(self.body_xpath+xpath)
        res = res or dict()
        for tr in trs:
            num = self._get_player_number(tr.xpath('td[1]')[0].text_content())
            if num:
                _d = res.get(num) or dict()
                for k,v in xpath_dict.items():
                    if tr.xpath(v):
                        if table_name == 'shots':
                            # убираем strong из верстки
                            _value = tr.xpath(v)[0].text_content().strip()
                        else:
                            _value = tr.xpath(v)[0].strip()
                            if table_name in ('gamingtime', 'extra'):
                                if table_name in k:
                                    # пересчет игрового времени в секунды
                                    _value = str2sec_safe(_value)
                                else:
                                    # строка в целое число
                                    _value = str2int_safe(_value)
                        _d[k] = _value
                res[num] = _d
        return res

    def _get_player_fivers(self, res):
        b'''Обновляем статистику игроков по номеру, добавляем пятерку,
            в которой заявлен игрок.
        '''
        if not self.teams:
            try:
                _teams = self.page_tree.xpath('//head/script[6]/text()'
                                )[0].split('\r\n'
                                )[5].split('var gamePlayers = '
                                )[1][:-1].replace('\'','"')
                _teams = json.loads(_teams)
                if _teams and isinstance(_teams, dict):
                    self.teams = {}
                    self.teams['hp'] = _teams.get('A')
                    self.teams['gp'] = _teams.get('B')
            except: pass
        for team_name, team in self.teams.items():
            for num in team.keys():
                player = res.get(team_name,{}).get(num)
                fiver = team.get(num, [0,0,0,0])[-1]
                if player and fiver:
                    player['fiver'] = str2int_safe(fiver)
        self.teams = None


class HockeyMHLMatchParser(GrabParser):
    b'''Парсер хоккейной статистики матча с сайта МХЛ'''
    url = xpathes.MHL_URL
    absolute_url = url
    pk_kwarg = 'idgame'
    as_get_param = True
    match_protocol_xpath = xpathes.MHL_MATCH_PROTOCOL_XPATH
    page_tree = None
    body_xpath = xpathes.MHL_BODY_XPATH
    xpath_dict = xpathes.MHL_MATCH_REPORT_DICT
    model_name = 'Match'
    adv_stats = None
    empty_page_text = xpathes.MHL_EMPTY_PAGE_TEXT
    body_notexists = xpathes.MHL_BODY_NOTEXISTS
    body_notexists_alt = xpathes.MHL_BODY_NOTEXISTS_ALT

    def put_data_in_db_from_page(self, id=None, data=None):
        b'''Основной метод, берующий данные со стороннего сайта и кладущий
            в БД, если все хорошо
        '''
        print(id, bool(data))
        if not data:
            data = self.get_page(id)
        if data and self.model_name:
            model = get_model('hockeyapp', self.model_name)
            print(id, bool(data))
            return model.objects.get_or_create_match(**data)

    def get_page(self, id=None):
        b'''  смотрим протокол матча '''
        self.page_tree = super(HockeyMHLMatchParser, self).get_page(id)
        if self.page_tree is not None:
            if self.page_tree.xpath(self.match_protocol_xpath):
                body = self.page_tree.xpath(self.match_protocol_xpath)[0]
                if body.text_content().find(self.empty_page_text) == -1:
                    #протокол игры существует
                    body = self.page_tree.xpath(self.body_xpath)[0]
                    body = body.text_content().encode('utf-8')
                    check = (   body.find(self.body_notexists) == -1 and
                                body.find(self.body_notexists_alt) == -1
                    )
                    if check:
                        #протокол найден, собираем данные
                        _html_body = self.g.response.unicode_body()
                        return self.get_match_all_data(id, html_body=_html_body)
            else:
                time.sleep(60)
                self.get_page(id)

    def _get_adv_stats(self, matchid):
        b''' Дополнительная статитстика по игрокам '''
        if matchid:
            self.adv_stats = AdvancedHockeyMatchParser().get_page(matchid)

    def get_match_all_data(self, matchid=None, html_body=None, url=None):
        b''' метод запускается, в случае если протокол игры существует и найден
            Забираем данные из протокола игры через DOM-дерево
        '''
        if self.page_tree is not None:
            self._get_adv_stats(matchid)
            _home_coach = self.get_home_team_coach()
            _guest_coach = self.get_guest_team_coach()
            _home_players = self.get_home_players()
            _guest_players = self.get_guest_players()
            _date = self.get_match_date()
            res = {
                    'khl_id': matchid,
                    'html_body': self.get_html_body(html_body),
                    'url': url if url else self.absolute_url,
                    'title': self.get_match_num(),
                    'spectators': self.get_spectators(),
                    'date': self.python_date(_date),
                    'count': self.get_match_count(),
                    'detail_count': self.get_match_detail_count(),
                    'judges': self.get_match_judges(),
                    'line_judges': self.get_match_line_judges(),
                    'home_team': {
                                    'title': self.get_home_team(),
                                    'region':  self.get_home_team_region(),
                                    'coach': _home_coach,
                                    'players': _home_players,
                                },
                    'home_coach': _home_coach,
                    'home_players': _home_players,
                    'guest_team': {
                                    'title': self.get_guest_team(),
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
            return res

    def python_date(self, date, month_dict = xpathes.MD):
        b''' парсит дату в datetime object '''
        if date:
            _date_dict = date.strip().lower().split(',')
            _dt = _date_dict[:2]
            _dt.append(_date_dict[3])
            _date_dict = _dt
            _m = _date_dict[0].split()[1].encode('utf-8')
            _date_dict[0] = _date_dict[0].replace(  _m.decode('utf-8'), 
                                                    month_dict.get(_m))
            if _date_dict[-1] != '':
                mask = '%d %m %Y %H:%M'
            else:
                mask = '%d %m %Y'
            _dt = ''.join(_date_dict).encode('utf-8')
            _dt = datetime.datetime.strptime(_dt, mask)
            return timezone.make_aware(_dt, current_tz)

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
        penalty_table = self._get_value('penalties_history')
        if penalty_table:
            lst = penalty_table[0].xpath('tr')
            return [self._get_penalty_data(tr) for tr in lst
                    if tr.attrib.get('class', '') not in (  'header', 
                                                            'report',
                                                            'first_row',
                                                        )
            ]
        else:
            return list()

    def _get_penalty_data(self, tr):
        b''' данные о штрафе '''
        _tds = tr.xpath('td')
        _ptype = _tds[3].text if _tds[3].text else _tds[8].text
        _dur = _tds[2].text if _tds[2].text else _tds[7].text
        _time = self._get_value_or_blank(tr.xpath('td[@class="time"]/strong'))
        res = {
                'time': _time,
                'duration': _dur.strip() if _dur else '',
                'ptype': _ptype.strip() if _ptype else '',
        }
        if tr.xpath('td/a'):
            _player = tr.xpath('td/a')[0].attrib.get('href','///'
                                                     ).split('/')[-2],
            if _player:
                res['player'] = isinstance(_player, tuple) and _player[0]

        return res

    def get_goals_history(self):
        b''' заброшенные шайбы '''
        goals_table = self._get_value('goals_history')
        if goals_table:
            return [self._get_goal_data(tr) for tr in goals_table[0].xpath('tr')
                    if tr.attrib.get('class', '') != 'header']
        else:
            return list()

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

    def get_home_players(self):
        b''' получаем игроков домашней команды '''
        _crtg = (   ('home_keepers', 1),
                    ('home_defenders', 2),
                    ('home_offenders', 3),
        )
        return self._get_players_list(_crtg, adv_stats_key='hp')

    def get_guest_players(self):
        b''' получаем игроков гостевой команды '''
        _crtg = (   ('guest_keepers', 1),
                    ('guest_defenders', 2),
                    ('guest_offenders', 3)
        )
        return self._get_players_list(_crtg, adv_stats_key='gp')

    def _get_players_list(self, crtg, adv_stats_key=''):
        res = list()
        for k,v in crtg:
            _plrs = self._get_players(k,v, adv_stats_key)
            if _plrs:
                res.extend(_plrs)
        return res

    def _get_players(self, key, line_type, ask=''):
        b''' получаем игроков команды '''
        plrs_table = self._get_value(key)
        if plrs_table:
            return (self._get_player_data(tr, line_type, ask) for tr 
                    in plrs_table[0].xpath('tr')
                    if tr.attrib.get('class', '') != 'header'
                    and self._get_player_data(tr, line_type))

    def _get_player_data(self, tr, line_type, adv_stats_key=''):
        b''' берем значения номер, id и тип игрока '''
        _raw_link = tr.xpath('td[@class="empty_bg"]/a')
        if not _raw_link:
            _raw_link = tr.xpath('td[@class="empty_bg left"]/a')
        if _raw_link:
            _raw_link = _raw_link[0]
            _num = tr.xpath('td[@class="empty_bg"]/strong/text()')
            if not _num:
                _num = tr.xpath('td[@class="empty_bg left"]/strong/text()')
            _num= _num[0] if _num else ''
            res = {
                    'number': _num,
                    'khl_id': _raw_link.attrib.get('href','').split('/')[-2],
                    'line': line_type,
                    'fio': _raw_link.text,
                    'stats': self._get_player_match_stats_by_line(tr,line_type),
            }
            if self.adv_stats and adv_stats_key:
                res['adv_stats'] = self.adv_stats.get(adv_stats_key,{}
                                                ).get(_num)
            return res

    def _get_player_match_stats_by_line(self, tr, line_type):
        b''' суммарная статистика игрока в матче '''
        if line_type > 1:
            return {
                    'goals': str2int_safe(tr.xpath('td[4]/text()')[0]),
                    'assists': str2int_safe(tr.xpath('td[5]/text()')[0]),
                    'points': str2int_safe(tr.xpath('td[6]/text()')[0]),
                    'plus_minus': str2int_safe(tr.xpath('td[7]/text()')[0]),
                    'penalty_time': str2int_safe(tr.xpath('td[8]/text()')[0]),
                    'ev_goals': str2int_safe(tr.xpath('td[9]/text()')[0]),
                    'pp_goals': str2int_safe(tr.xpath('td[10]/text()')[0]),
                    'es_goals': str2int_safe(tr.xpath('td[11]/text()')[0]),
                    'overtime_goals': str2int_safe(tr.xpath('td[12]/text()')[0]),
                    'win_goals': str2int_safe(tr.xpath('td[13]/text()')[0]),
                    'bullet_goals': str2int_safe(tr.xpath('td[14]/text()')[0]),
                    'shots': str2int_safe(tr.xpath('td[15]/text()')[0]),
                    'pis': str2float_safe(tr.xpath('td[16]/text()')[0]),
                    'faceoff': str2int_safe(tr.xpath('td[17]/text()')[0]),
                    'winfaceoff': str2int_safe(tr.xpath('td[18]/text()')[0]),
                    'winfaceoff_p': str2float_safe(tr.xpath('td[19]/text()')[0]),
            }
        else:
            return {
                    'shots': str2int_safe(tr.xpath('td[7]/text()')[0]),
                    'loose_goals': str2int_safe(tr.xpath('td[8]/text()')[0]),
                    'saves': str2int_safe(tr.xpath('td[9]/text()')[0]),
                    'saves_p': str2float_safe(tr.xpath('td[10]/text()')[0]),
                    'sf': str2float_safe(tr.xpath('td[11]/text()')[0]),
                    'gamingtime': str2sec_safe(tr.xpath('td[15]/text()')[0]),
            }

    def get_match_num(self):
        b''' возьмем значение номера матча '''
        _res = self._get_value('match_num')
        return _res[0].strip().split('.')[0] if _res else ''

    def get_match_date(self):
        b''' возьмем значение даты матча '''
        _res = self._get_value('match_date')
        return _res[0].strip().split('.')[1] if _res else ''

    def get_spectators(self):
        b''' возьмем значение посещаемости '''
        _res = self._get_value('match_spectators')
        return str2int_safe(_res[0].split(':')[1].strip().split()[0])

    def get_home_team(self):
        b''' получаем имя домашней команды '''
        _res = self._get_value('home_team')
        return _res[0].strip() if _res else ''

    def get_home_team_region(self):
        b''' получаем регион домашней команды '''
        _res = self._get_value('home_team_region')
        return _res[0].strip()[1:-1] if _res else ''

    def get_home_team_coach(self):
        b''' получаем тренера домашней команды '''
        _res = self._get_value('home_team_coach')
        return _res[0].strip() if _res else ''

    def get_guest_team(self):
        b''' получаем имя гостевой команды '''
        _res = self._get_value('guest_team')
        return _res[0].strip() if _res else ''

    def get_guest_team_region(self):
        b''' получаем регион гостевой команды '''
        _res = self._get_value('guest_team_region')
        return _res[0].strip()[1:-1] if _res else ''

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
            _res = _res[0].text_content().strip().split('          ')
        if _res and len(_res)>1:
            if len(_res) < 3:
                return [_res[1].strip()]
            else:
                return [_res[1].strip(), _res[3].strip()]
        return ''

    def get_match_line_judges(self):
        b''' получаем линейных судей матча '''
        _res = self._get_value('match_line_judges')
        if _res:
            _res = _res[0].text_content().strip().split('\n')
            return [j.strip() for j in _res[1:]]
        return ''
################################################################################
################################################################################
################################################################################


class HockeyMHL2MatchParser(HockeyMHLMatchParser):
    b'''Парсер хоккейной статистики матча с сайта МХЛ-2'''
    url = xpathes.MHL2_URL
    absolute_url = url
    match_protocol_xpath = xpathes.MHL2_MATCH_PROTOCOL_XPATH
    body_xpath = xpathes.MHL2_BODY_XPATH
    xpath_dict = xpathes.MHL2_MATCH_REPORT_DICT

    def python_date(self, date, month_dict = xpathes.MD):
        b''' парсит дату в datetime object '''
        print('!{}!'.format(date))
        if date:
            _date_dict = date.strip().lower().split(',')
            _dt = _date_dict[:1]
            _dt.append(_date_dict[2])
            _date_dict = _dt
            _m = _date_dict[0].split()[1].encode('utf-8')
            _date_dict[0] = _date_dict[0].replace(  _m.decode('utf-8'), 
                                                    month_dict.get(_m))
            if _date_dict[-1] != '':
                mask = '%d %m %Y %H:%M'
            else:
                mask = '%d %m %Y'
            _dt = ''.join(_date_dict).encode('utf-8')
            _dt = datetime.datetime.strptime(_dt, mask)
            return timezone.make_aware(_dt, current_tz)
################################################################################
################################################################################
################################################################################


class HockeyKHLMatchParser(HockeyMHLMatchParser):
    b'''Парсер хоккейной статистики матча с сайта КХЛ'''
    url = xpathes.KHL_MATCH_URL
    absolute_url = url
    pk_kwarg = 'id'
    as_get_param = False
    match_protocol_xpath = xpathes.KHL_MATCH_PROTOCOL_XPATH
    body_xpath = xpathes.KHL_MATCH_PROTOCOL_XPATH
    xpath_dict = xpathes.KHL_MATCH_REPORT_DICT

    def get_page(self, id=None):
        b'''  смотрим протокол матча '''
        _id = str(id)+'/protocol'
        self.page_tree = GrabParser.get_page(self, _id)
        if self.page_tree is not None:
            if self.page_tree.xpath(self.match_protocol_xpath):
                body = self.page_tree.xpath(self.match_protocol_xpath)[0]
                if body.text_content().strip():
                    #протокол игры существует
                    #протокол найден, собираем данные
                    _html_body = self.g.response.unicode_body()
                    return self.get_match_all_data( html_body=_html_body,
                                                    matchid=id)
            else:
                time.sleep(60)
                self.get_page(id)

    def get_spectators(self):
        b''' возьмем значение посещаемости '''
        _res = self._get_value('match_spectators')
        return str2int_safe(_res[0].strip().split()[0])

    def python_date(self, date, month_dict = xpathes.MDP):
        b''' парсит дату в datetime object '''
        if date:
            _date_dict = date.strip().lower().split(',')
            _dt = _date_dict[:1]
            _dt.append(_date_dict[2])
            _date_dict = _dt
            _m = _date_dict[0].split()[1].encode('utf-8')
            _date_dict[0] = _date_dict[0].replace(  _m.decode('utf-8'), 
                                                    month_dict.get(_m))
            if _date_dict[-1] != '':
                mask = '%d %m %Y %H:%M'
            else:
                mask = '%d %m %Y'
            _dt = ''.join(_date_dict).encode('utf-8')
            _dt = datetime.datetime.strptime(_dt, mask)
            return timezone.make_aware(_dt, current_tz)

    def get_match_judges(self):
        b''' получаем судей матча '''
        _res = self._get_value('match_judges')
        if _res:
            _res = _res[0].split(',')
            return [j.strip() for j in _res]
        return ''

    def get_match_line_judges(self):
        b''' получаем линейных судей матча '''
        _res = self._get_value('match_line_judges')
        if _res:
            _res = _res[0].split(',')
            return [j.strip() for j in _res]
        return ''

    def get_home_team_coach(self):
        b''' получаем тренера домашней команды '''
        _res = self._get_value('home_team_coach')
        return _res[0].split(':')[1].strip() if _res else ''

    def get_guest_team_coach(self):
        b''' получаем тренера гостевой команды '''
        _res = self._get_value('guest_team_coach')
        return _res[0].split(':')[1].strip() if _res else ''

    def get_goals_history(self):
        b''' заброшенные шайбы '''
        goals_data = self._get_value('goals_history')
        if goals_data:
            goals_data = khl_string_data2python_obj_safe(goals_data[0])
            return [self._get_goal_data(item) for item in goals_data]
        else:
            return list()

    def _get_goal_data(self, item):
        b''' данные о заброшенной шайбе '''
        _parity = _PARITTYDICT.get(item[4].encode('utf-8'),0)
        res = {
                'period': item[1].strip(),
                'time': item[2].strip(),
                'parity': _parity,
                'scorer': fromstring(item[5]).attrib.get('href',''
                                            ).split('/')[-2],
                'assist': self._get_assist(item),
                'home_five_numbers': self._get_five_numbers(item[8]),
                'guest_five_numbers': self._get_five_numbers(item[9]),
        }
        return res

    def _get_assist(self, item):
        b''' ассистенты '''
        res = []
        for i in item[6],item[7]:
            if i:
                res.append(fromstring(i).attrib.get('href','').split('/')[-2])
        return set(res)

    def _get_five_numbers(self, string):
        b''' игроки на поле при заброшенной шайбе '''
        return ','.join([fromstring(i).text for i in string.split(',')
                                            if i and fromstring(i).text
            ])

    def get_penalties_history(self):
        b''' штрафы '''
        penalty_table = self._get_value('penalties_history')
        if penalty_table:
            lst = penalty_table[0].xpath('tbody/tr')
            return [self._get_penalty_data(tr) for tr in lst
                    if tr.attrib.get('class', '') not in ('group',)
            ]
        else:
            return list()

    def _get_penalty_data(self, tr):
        b''' данные о штрафе '''
        _tds = tr.xpath('td')
        if _tds[0].text:
            _ptype = _tds[3].text
            _dur = _tds[2].text
            _time = _tds[0].text
        else:
            _ptype = _tds[4].text
            _dur = _tds[3].text
            _time = _tds[1].text
        res = {
                'time': _time.strip() if _time else '',
                'duration': _dur.strip() if _dur else '',
                'ptype': _ptype.strip() if _ptype else '',
        }
        if tr.xpath('td/a'):
            _player = tr.xpath('td/a')[0].attrib.get('href','///'
                                                     ).split('/')[-2],
            if _player:
                res['player'] = isinstance(_player, tuple) and _player[0]
        return res

    def _get_khl_string_data(self, key):
        return {
                'home_keepers': 0,
                'home_defenders': 1,
                'home_offenders': 2,
                'guest_keepers': 3,
                'guest_defenders': 4,
                'guest_offenders': 5,
        }.get(key)

    def _get_players(self, key, line_type, ask=''):
        b''' получаем игроков команды '''
        plrs_data = self._get_value(key)
        if plrs_data:
            place = self._get_khl_string_data(key)
            plrs_data = khl_string_data2python_obj_safe(plrs_data[place])
            return (self._get_player_data(item, line_type, ask) for item in plrs_data)

    def _get_player_data(self, item, line_type, adv_stats_key=''):
        b''' берем значения номер, id и тип игрока '''
        _num = fromstring(item[0]).text.strip()
        _plr = item[1] if item[1][-1]=='>' else item[1].split('</a>')[0]+'</a>'
        res = {
                'number': _num,
                'khl_id': fromstring(_plr).attrib.get('href','///'
                                                    ).split('/')[-2],
                'line': line_type,
                'fio': fromstring(_plr).text.strip(),
                'stats': self._get_player_match_stats_by_line(item,line_type),
        }
        if self.adv_stats and adv_stats_key:
            res['adv_stats'] = self.adv_stats.get(adv_stats_key,{}
                                            ).get(_num)
        return res

    def _get_player_match_stats_by_line(self, item, line_type):
        b''' суммарная статистика игрока в матче '''
        if line_type > 1:
            return {
                    'goals': str2int_safe(item[3]),
                    'assists': str2int_safe(item[4]),
                    'points': str2int_safe(item[5]),
                    'plus_minus': str2int_safe(item[6]),
                    'penalty_time': str2int_safe(item[7]),
                    'ev_goals': str2int_safe(item[8]),
                    'pp_goals': str2int_safe(item[9]),
                    'es_goals': str2int_safe(item[10]),
                    'overtime_goals': str2int_safe(item[11]),
                    'win_goals': str2int_safe(item[12]),
                    'bullet_goals': str2int_safe(item[13]),
                    'shots': str2int_safe(item[14]),
                    'pis': str2float_safe(item[15]),
                    'faceoff': str2int_safe(item[16]),
                    'winfaceoff': str2int_safe(item[17]),
                    'winfaceoff_p': str2float_safe(item[18]),
                    'gamingtime': str2sec_safe(item[19]),
                    'change_count': str2int_safe(item[20]),
                    'hits': str2int_safe(item[21]),
                    'blocks': str2int_safe(item[22]),
                    'fouls': str2int_safe(item[23]),
            }
        else:
            return {
                    'shots': str2int_safe(item[6]),
                    'loose_goals': str2int_safe(item[7]),
                    'saves': str2int_safe(item[8]),
                    'saves_p': str2float_safe(item[9]),
                    'sf': str2float_safe(item[10]),
                    'gamingtime': str2sec_safe(item[15]),
            }
################################################################################
################################################################################
################################################################################


class HockeyVHLMatchParser(HockeyMHLMatchParser):
    b'''Парсер хоккейной статистики матча с сайта ВХЛ'''
    url = xpathes.VHL_MATCH_URL
    absolute_url = url
    match_protocol_xpath = xpathes.VHL_MATCH_PROTOCOL_XPATH
    body_xpath = xpathes.VHL_MATCH_PROTOCOL_XPATH
    xpath_dict = xpathes.VHL_MATCH_REPORT_DICT

    def python_date(self, date, month_dict = xpathes.MD_EN):
        b''' парсит дату в datetime object '''
        if date:
            _date_dict = date.strip().lower().split(',')
            _dt = _date_dict[:1]
            _dt.append(_date_dict[2])
            _date_dict = _dt
            _m = _date_dict[0].split()[1].encode('utf-8')
            _date_dict[0] = _date_dict[0].replace(  _m.decode('utf-8'), 
                                                    month_dict.get(_m))
            if _date_dict[-1] != '':
                mask = '%d %m %Y %H:%M'
            else:
                mask = '%d %m %Y'
            _dt = ''.join(_date_dict).encode('utf-8')
            _dt = datetime.datetime.strptime(_dt, mask)
            return timezone.make_aware(_dt, current_tz)

    def get_match_line_judges(self):
        b''' получаем линейных судей матча '''
        _res = self._get_value('match_line_judges')
        if _res:
            _res = _res[0].text_content().strip().split('\n')
            return [j.strip() for j in _res[-2:]]
        return ''

    def get_home_team_coach(self):
        b''' получаем тренера домашней команды '''
        _res = self._get_value('home_team_coach')
        if _res:
            _res = _res[0].text_content().strip()
            return _res.split(':')[1].strip()
        return ''

    def get_guest_team_coach(self):
        b''' получаем тренера гостевой команды '''
        _res = self._get_value('guest_team_coach')
        if _res:
            _res = _res[0].text_content().strip()
            return _res.split(':')[1].strip()
        return ''