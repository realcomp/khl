#coding: utf-8
from __future__ import print_function, unicode_literals

__author__='smirnov.ev'

import datetime

from django.db.models.loading import get_model
from django.utils import timezone
current_tz = timezone.get_current_timezone()

from base.utils import str2int_safe

from . import GrabParser
from . import xpathes


class KHLScheduleParser(GrabParser):
    b''' Парсер расписания матчей КХЛ '''
    model_name = 'Schedule'
    url = xpathes.KHL_SITE_URL
    absolute_url = url+'/calendar/??/00'
    as_get_param = False
    body_xpath = xpathes.KHL_MATCH_PROTOCOL_XPATH
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
        #if id:
            #self.absolute_url = self.absolute_url.replace('??', str(id))
        return self.absolute_url

    def put_data_in_db_from_page(self, id=None, update=False, 
                                challenge=None, challenge_type=False
        ):
        b'''Основной метод, берующий данные со стороннего сайта и кладущий
            в БД, если все хорошо
        ''' 
        data = self.get_page(id)
        if data and self.model_name:
            model = get_model('hockeyapp', self.model_name)
            if challenge_type: data['challenge_type'] = challenge_type
            if challenge: data['challenge'] = challenge
            model.objects.create_or_update_schedule(**data)

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
        if self.date:
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
            'title': mdiv.xpath(self.mxd['ru_title'])[0],
            'date': self.python_date(_time),
            'home_team': mdiv.xpath(self.mxd['home_team'])[0].strip(),
            'guest_team': mdiv.xpath(self.mxd['guest_team'])[0].strip(),
            'khl_id': str2int_safe(khl_id),
        }
        return match

    def python_date(self, date, month_dict = xpathes.MDP):
        b''' парсит дату в datetime object '''
        if date:
            _date_dict = date.strip().lower().split(',')
            _m = _date_dict[0].split()[1].encode('utf-8')
            month = month_dict.get(_m)
            if month: 
                _date_dict[0] = _date_dict[0].replace(_m.decode('utf-8'), month)
            else:
                _date_dict[0] = _date_dict[0][:3]+'01'+_date_dict[0][3:]
            if _date_dict[-1] != '':
                mask = '%d %m %Y %H:%M'
            else:
                mask = '%d %m %Y'
            _dt = ''.join(_date_dict).encode('utf-8')
            _dt = datetime.datetime.strptime(_dt, mask)
            return timezone.make_aware(_dt, current_tz)

    def start_date(self, date):
        b''' возвращает дату начала сезона '''
        if date:
            _pdt = date
            _year = _pdt.year - 1 if _pdt.month < 7 else _pdt.year
            _dt = datetime.datetime(day=1, month=7, year=_year)
            return timezone.make_aware(_dt, current_tz)

    def end_date(self, date):
        b''' возвращает дату окончания сезона '''
        if date:
            _pdt = date
            _year = _pdt.year + 1 if _pdt.month > 6 else _pdt.year
            _dt =  datetime.datetime(day=30, month=6, year=_year)
            return timezone.make_aware(_dt, current_tz)
################################################################################
################################################################################
################################################################################


class VHLScheduleParser(KHLScheduleParser):
    b''' Парсер расписания матчей ВХЛ '''
    url = xpathes.VHL_SITE_URL
    absolute_url = url+'/calendar/??/season/0/'
    body_xpath = xpathes.VHL_MATCH_PROTOCOL_XPATH+'/div[@id="laConteiner"]/div[@class="inner_content"]'
    match_protocol_xpath = body_xpath
    xpath_dict = {
                    'matches': "/div[@class='matches_list']/table[@class='uni_table matches']/tr"
    }
    mxd = {
                    'ru_title': 'td[@class="col_number left"]/text()',
                    'ru_title_alt': 'td[@class="col_number left"]/p/text()',
                    'date': 'td[@class="date"]/h4/text()',
                    'home_team': 'td[@class="col_team left"]/a[1]/text()',
                    'guest_team': 'td[@class="col_team left"]/a[2]/text()',
                    'home_team_alt': 'td[@class="col_team left"]/a/b/text()',
                    'guest_team_alt': 'td[@class="col_team left"]/a/b/text()',
                    'khl_id': 'td[@class="col_online"]/a/@href',
    }

    def get_calendar(self, html_body=None):
        b''' Словарь календаря '''
        res = super(VHLScheduleParser, self).get_calendar(html_body)
        res['league'] = 'VHL'
        return res

    def get_matches(self):
        data = self._get_value('matches')
        res = []
        for tr in data:
            if tr.attrib.get('class') != 'header':
                date = tr.xpath(self.mxd['date'])[0].strip()
                date = datetime.datetime.strptime(date, '%d.%m.%y')
                for mcapsula in tr.xpath("td[@class='number']/table/tr"):
                    match = self._get_match_info(mcapsula, date)
                    res.append(match)
        self.date = match['date']
        return res

    def _get_match_info(self, mcapsula, date):
        if mcapsula.xpath(self.mxd['home_team']):
            home_team = mcapsula.xpath(self.mxd['home_team'])[0]
            guest_team = mcapsula.xpath(self.mxd['guest_team_alt'])
            if guest_team:
                guest_team = guest_team[0]
            else:
                guest_team = mcapsula.xpath(self.mxd['guest_team'])[0]
        else:
            home_team = mcapsula.xpath(self.mxd['home_team_alt'])[0]
            guest_team = mcapsula.xpath(self.mxd['guest_team'])
            if guest_team:
                guest_team = guest_team[0]
            else:
                guest_team = mcapsula.xpath(self.mxd['guest_team_alt'])[0]
        match = {
            'title': self._get_title(mcapsula),
            'date': date,
            'home_team': home_team,
            'guest_team': guest_team,
            'khl_id': str2int_safe(self._get_khl_id(mcapsula)),
        }
        return match

    def _get_title(self, mcapsula):
        if mcapsula.xpath(self.mxd['ru_title']):
            return mcapsula.xpath(self.mxd['ru_title'])[0]
        else:
            return mcapsula.xpath(self.mxd['ru_title_alt'])[0]

    def _get_khl_id(self, mcapsula):
        khl_id = mcapsula.xpath(self.mxd['khl_id'])
        return khl_id[0].split('/')[4].split('.')[0] if khl_id else ''
################################################################################
################################################################################
################################################################################


class MHLScheduleParser(VHLScheduleParser):
    b''' Парсер расписания матчей MХЛ '''
    url = xpathes.MHL_SITE_URL
    absolute_url = url+'/calendar/??/0/'
    body_xpath = xpathes.MHL_MATCH_PROTOCOL_XPATH+'/div[@id="laConteiner"]/div[@class="inner_content"]'
    match_protocol_xpath = body_xpath
    xpath_dict = {
                    'matches': "/div[@class='matches_list']/table[@class='matches_table']/tr"
    }
    mxd = {
                    'ru_title': 'td[@class="col_number"]/text()',
                    'ru_title_alt': 'td[@class="col_number"]/p/text()',
                    'date': 'td[@class="date"]/h4/text()',
                    'home_team': 'td[@class="col_team"]/a[1]/text()',
                    'guest_team': 'td[@class="col_team"]/a[2]/text()',
                    'home_team_alt': 'td[@class="col_team"]/a/b/text()',
                    'guest_team_alt': 'td[@class="col_team"]/a/b/text()',
                    'khl_id': 'td[@class="col_online"]/a/@href',
    }

    def get_calendar(self, html_body=None):
        b''' Словарь календаря '''
        res = super(MHLScheduleParser, self).get_calendar(html_body)
        res['league'] = 'MHL'
        return res
################################################################################
################################################################################
################################################################################


class MHL2ScheduleParser(MHLScheduleParser):
    b''' Парсер расписания матчей MХЛ-2 '''
    url = xpathes.MHL2_SITE_URL
    absolute_url = url+'/calendar/??/0/'
    body_xpath = '//div[@id="wrapper"]/div[@class="content"]/div[@class="leftBlockInside"]/div[@class="second_content"]'
    match_protocol_xpath = body_xpath
    mxd = {
                    'ru_title': 'td[@class="col_number"]/text()',
                    'ru_title_alt': 'td[@class="col_number"]/p/text()',
                    'date': 'td[@class="date"]/h4/text()',
                    'home_team': 'td[@class="col_team"]/a[1]/text()',
                    'guest_team': 'td[@class="col_team"]/a[2]/text()',
                    'home_team_alt': 'td[@class="col_team"]/a/strong/b/text()',
                    'guest_team_alt': 'td[@class="col_team"]/a/strong/b/text()',
                    'khl_id': 'td[@class="col_online"]/a/@href',
    }

    def get_calendar(self, html_body=None):
        b''' Словарь календаря '''
        res = super(MHL2ScheduleParser, self).get_calendar(html_body)
        res['league'] = 'MHL-2'
        return res