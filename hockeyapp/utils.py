#coding: utf-8
from __future__ import print_function
import grab

#from django.conf import settings
from .defaults import DEFAULT_KHL_MATCH_PROTOCOL_XPATH, DEFAULT_BODY_NOTEXISTS
from .defaults import DEFAULT_EMPTY_PAGE_TEXT, DEFAULT_BODY_XPATH

from .models import Match


class HockeyMatchParser(object):
    b'''
        Парсер хоккейной статистики
    '''
    url = 'http://mhl.khl.ru/report/272/'
    match_pk_kwarg = 'idgame'
    as_get_param = True
    match_protocol_xpath = DEFAULT_KHL_MATCH_PROTOCOL_XPATH
    page_tree = None
    body_xpath = DEFAULT_BODY_XPATH

    def put_data_in_db_from_page(self, matchid=None):
        b'''Основной метод, берующий данные со стороннего сайта и кладущий
            в БД, если все хорошо
        ''' 
        data = self.get_page(matchid)
        if data:
            return Match.objects.get_or_create_match(**data)

    def get_page(self, matchid=None):
        matchid = self.url and self.match_pk_kwarg and matchid
        if matchid:
            _absurl = '{0}?{1}={2}'.format(self.url,self.match_pk_kwarg,matchid)
            g = grab.Grab(url=_absurl)
            # забираем ответ от ресурса
            try:
                g.go(_absurl)
            except grab.error.GrabNetworkError: 
                g = None
            if g and g.response.code == 200:
                # страница доступна
                self.page_tree = g.tree
                #TODO: жрет много ресурсов, лучше переделать 
                body = self.page_tree.xpath(self.match_protocol_xpath)[0]
                if body.text_content().find(DEFAULT_EMPTY_PAGE_TEXT) == -1:
                    #протокол игры существует
                    body = self.page_tree.xpath(self.body_xpath)[0]
                    body = body.text_content().encode('utf-8')
                    if body.find(DEFAULT_BODY_NOTEXISTS) == -1:
                        #протокол найден, собираем данные
                        return self.get_all_data(matchid)

    def get_all_data(self, matchid=None):
        b''' метод запускается, в случае если протокол игры существует и найден
            Забираем данные из протокола игры через DOM-дерево
        '''
        if self.page_tree is not None:
            res = {
                    'khl_id': matchid,
                    'title': self.get_match_num(),
                    'spectators': self.get_spectators(),
                    'date': self.get_match_date(),
                    'count': self.get_match_count(),
                    'detail_count': self.get_match_detail_count(),
                    'judges': self.get_match_judges(),
                    'line_judges': self.get_match_line_judges(),
                    'home_team': {
                                    'title': self.get_home_team(),
                                    'region':  self.get_home_team_region(),
                                    'coach': self.get_home_team_coach(),
                                },
                    'guest_team': {
                                    'title': self.get_guest_team(),
                                    'region':  self.get_guest_team_region(),
                                    'coach': self.get_guest_team_coach(),
                                },
            }
            return res

    def get_match_num_xpath(self):
        b''' путь до имени матча '''
        _xpath = self.body_xpath or ''
        return _xpath+'//div[@class="games_title"]//p'

    def get_match_num(self):
        b''' возьмем значение номера матча '''
        _res = self.page_tree.xpath(self.get_match_num_xpath())
        return _res[0].text.split('.')[0] if _res else ''

    def get_match_date_xpath(self):
        b''' путь до даты матча '''
        _xpath = self.body_xpath or ''
        return _xpath+'//div[@class="games_title"]//p'

    def get_match_date(self):
        b''' возьмем значение даты матча '''
        _res = self.page_tree.xpath(self.get_match_date_xpath())
        return _res[0].text.split('.')[1] if _res else ''

    def get_spectators_xpath(self):
        b''' путь до посещаемости матча '''
        _xpath = self.body_xpath or ''
        return _xpath+'//div[@class="games_title"]//p[@class="games_title_more"]'

    def get_spectators(self):
        b''' возьмем значение посещаемости '''
        _res = self.page_tree.xpath(self.get_spectators_xpath())
        return _res[0].text.split(':')[1] if _res else ''

    def get_home_team_xpath(self):
        b''' путь до имя домашней команды '''
        return ''.join((self.body_xpath or '',
                        '//table[@class="matches_protocol_main"][1]',
                        '/tr[@class="first_row"]/td[@class="first_column"]/h2'))

    def get_home_team(self):
        b''' получаем имя домашней команды '''
        _res = self.page_tree.xpath(self.get_home_team_xpath())
        return _res[0].text if _res else ''

    def get_home_team_region_xpath(self):
        b''' путь до регион домашней команды '''
        return ''.join((self.body_xpath or '',
                        '//table[@class="matches_protocol_main"][1]',
                        '/tr[@class="first_row"]/td[@class="first_column"]',
                        '/p/strong'))

    def get_home_team_region(self):
        b''' получаем регион домашней команды '''
        _res = self.page_tree.xpath(self.get_home_team_region_xpath())
        return _res[0].text[1:-1] if _res else ''

    def get_home_team_coach_xpath(self):
        b''' путь до тренера домашней команды '''
        return ''.join((self.body_xpath or '',
                        '//table[@class="matches_protocol_main"][2]',
                        '/tr[@class="second_row"]/td[@class="first_column"]',
                        '/p/text()'))

    def get_home_team_coach(self):
        b''' получаем тренера домашней команды '''
        _res = self.page_tree.xpath(self.get_home_team_coach_xpath())
        if _res:
            return _res[0].replace('\n', '').replace('  ','')
        return ''

    def get_guest_team_xpath(self):
        b''' путь до имя гостевой команды '''
        return ''.join((self.body_xpath or '',
                        '//table[@class="matches_protocol_main"][1]',
                        '/tr[@class="first_row"]/td[@class="right_column"]/h2'))

    def get_guest_team(self):
        b''' получаем имя гостевой команды '''
        _res = self.page_tree.xpath(self.get_guest_team_xpath())
        return _res[0].text if _res else ''

    def get_guest_team_region_xpath(self):
        b''' путь до регион гостевой команды '''
        return ''.join((self.body_xpath or '',
                        '//table[@class="matches_protocol_main"][1]',
                        '/tr[@class="first_row"]/td[@class="right_column"]',
                        '/p/strong'))

    def get_guest_team_region(self):
        b''' получаем регион гостевой команды '''
        _res = self.page_tree.xpath(self.get_guest_team_region_xpath())
        return _res[0].text[1:-1] if _res else ''

    def get_guest_team_coach_xpath(self):
        b''' путь до тренера гостевой команды '''
        return ''.join((self.body_xpath or '',
                        '//table[@class="matches_protocol_main"][2]',
                        '/tr[@class="second_row"]/td[@class="right_column"]',
                        '/p/text()'))

    def get_guest_team_coach(self):
        b''' получаем тренера гостевой команды '''
        _res = self.page_tree.xpath(self.get_guest_team_coach_xpath())
        if _res:
            return _res[0].replace('\n', '').replace('  ','')
        return ''

    def get_match_count_xpath(self):
        b''' путь до счета матча '''
        return ''.join((self.body_xpath or '',
                        '//table[@class="matches_protocol_main"][2]',
                        '/tr[@class="second_row"]/td[@class="main_column"]',
                        '/p[@class="count"]/span/text()'))

    def get_match_count(self):
        b''' получаем счет матча '''
        _res = self.page_tree.xpath(self.get_match_count_xpath())
        if _res:
            return _res[0].replace('\n', '').replace(' ','')
        return ''

    def get_match_detail_count_xpath(self):
        b''' путь до детального счета матча '''
        return ''.join((self.body_xpath or '',
                        '//table[@class="matches_protocol_main"][2]',
                        '/tr[@class="second_row"]/td[@class="main_column"]',
                        '/div[@class="detail_count"]/text()'))

    def get_match_detail_count(self):
        b''' получаем детальный счет матча '''
        _res = self.page_tree.xpath(self.get_match_detail_count_xpath())
        if _res:
            return _res[0].replace('\n', '').replace(' ',',')
        return ''

    def get_match_judges_xpath(self):
        b''' путь до судей матча '''
        return ''.join((self.body_xpath or '',
                        '//table[@class="matches_protocol_main"][2]',
                        '/tr[@class="second_row"]/td[@class="main_column"]',
                        '/p[2]'))

    def get_match_judges(self):
        b''' получаем судей матча '''
        _res = self.page_tree.xpath(self.get_match_judges_xpath())
        if _res:
            _res = _res[0].text_content().replace('  ','').split('\n',)[1:]
            return _res
        return ''

    def get_match_line_judges_xpath(self):
        b''' путь до линейных судей матча '''
        return ''.join((self.body_xpath or '',
                        '//table[@class="matches_protocol_main"][2]',
                        '/tr[@class="second_row"]/td[@class="main_column"]',
                        '/p[3]'))

    def get_match_line_judges(self):
        b''' получаем линейных судей матча '''
        _res = self.page_tree.xpath(self.get_match_line_judges_xpath())
        if _res:
            _res = _res[0].text_content().replace('  ','').split('\n',)[1:]
            return _res
        return ''