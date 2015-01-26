#coding: utf-8
from __future__ import print_function, unicode_literals

__author__='smirnov.ev'

import datetime

from django.db.models.loading import get_model
from base.utils import str2int_safe

from .. import defaults

from . import GrabParser


class KHLScheduleParser(GrabParser):
    b''' Парсер расписания матчей КХЛ '''
    model_name = 'Schedule'
    url = defaults.KHL_SITE_URL
    absolute_url = url+'/calendar/??/00'
    as_get_param = False
    body_xpath = defaults.KHL_MATCH_PROTOCOL_XPATH
    match_protocol_xpath = body_xpath
    xpath_dict = {
                    'matches': "/div"
    }
    mxd = {
                    'ru_title': 'div[@class="top"]/div[@class="left"]/text()',
                    'time': 'div[@class="top"]/div[@class="right"]/text()',
                    'home_team': 'table/tr[1]/td/text()',
                    'guest_team': 'table/tr[2]/td/text()',
                    'future_khl_id': 'div/a[@class="text"]/@href',
                    'past_khl_id': 'div/div[@class="expand"]/ul/li/a[@class="text"][1]/@href',
    }

    def _get_absolute_url(self, id=None, slash=True):
        b'''определяем url страницы
            По-умолчанию: self.absolute_url = self.url
        '''
        if id:
            self.absolute_url = self.absolute_url.replace('??', str(id))
        return self.absolute_url

    def put_data_in_db_from_page(self, id=None):
        b'''Основной метод, берующий данные со стороннего сайта и кладущий
            в БД, если все хорошо
        ''' 
        data = self.get_page(id)
        if data and self.model_name:
            model = get_model('hockeyapp', self.model_name)
            model.objects.create_schedule(**data)

    def get_page(self, id=None):
        b'''  смотрим страницу календаря '''
        self.page_tree=super(KHLScheduleParser, self).get_page(id,False)
        if self.page_tree is not None:
            if self.page_tree.xpath(self.match_protocol_xpath):
                _html_body = self.g.response.unicode_body()
                return self.get_calendar(_html_body)

    def get_calendar(self, html_body=None):
        b''' Словарь календаря '''
        res = {
                'matches': self.get_matches(),
                'league': 'KHL',
                'url': self.absolute_url,
                #'html_body': self.get_html_body(html_body),
        }
        res['season'] = { 
                            'start_date':self.start_date(self.date),
                            'end_date': self.end_date(self.date),
                }
        return res

    def get_matches(self):
        data = self._get_value('matches')
        res = []
        for div in data:
            if div.attrib.get('class') == 'matchDate':
                date = div.xpath("div/strong/text()")[0].strip()
            elif div.attrib.get('class') == 'matches':
                for mdiv in div.xpath("div[@class='row']/div"):
                    match = self._get_match_info(mdiv, date)
                    res.append(match)
        self.date = match['date']
        return res

    def _get_match_info(self, mdiv, date):
        _time = mdiv.xpath(self.mxd['time'])[0].strip().split()[0]
        _time = '{} {}'.format(date, _time)
        khl_id = mdiv.xpath(self.mxd['future_khl_id'])
        if not khl_id:
            khl_id = mdiv.xpath(self.mxd['past_khl_id'])
        khl_id = khl_id[0].split('/')[3] if khl_id else ''
        match = {
            'ru_title': mdiv.xpath(self.mxd['ru_title'])[0],
            'date': self.python_date(_time),
            'home_team': mdiv.xpath(self.mxd['home_team'])[0],
            'guest_team': mdiv.xpath(self.mxd['guest_team'])[0],
            'khl_id': str2int_safe(khl_id),
        }
        return match

    def python_date(self, date, month_dict = defaults.MDP):
        b''' парсит дату в datetime object '''
        if date:
            _date_dict = date.strip().lower().split(',')
            _m = _date_dict[0].split()[1].encode('utf-8')
            _date_dict[0] = _date_dict[0].replace(  _m.decode('utf-8'), 
                                                    month_dict.get(_m))
            if _date_dict[-1] != '':
                mask = '%d %m %Y %H:%M'
            else:
                mask = '%d %m %Y'
            _dt = ''.join(_date_dict).encode('utf-8')
            return datetime.datetime.strptime(_dt, mask)

    def start_date(self, date):
        b''' возвращает дату начала сезона '''
        _pdt = date
        _year = _pdt.year - 1 if _pdt.month < 7 else _pdt.year
        return datetime.datetime(day=1, month=7, year=_year)

    def end_date(self, date):
        b''' возвращает дату окончания сезона '''
        _pdt = date
        _year = _pdt.year + 1 if _pdt.month > 6 else _pdt.year
        return datetime.datetime(day=30, month=6, year=_year)