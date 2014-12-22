#coding: utf-8
from __future__ import unicode_literals

# MATCH
BODY_NOTEXISTS = b'Протокол не найден'
EMPTY_PAGE_TEXT = 'Fatal error'
KHL_MATCH_PROTOCOL_XPATH = '//div[@class="content"]//div[@class="b-left"]//div[@class="second_content"]'
URL = 'http://mhl.khl.ru/report/272/'
KHL_SITE_URL =  'http://www.khl.ru'

BODY_XPATH = KHL_MATCH_PROTOCOL_XPATH+'//div[@class="inner_content"]'

_MMP_XPATH = '//table[@class="matches_protocol_main"]' #xpath match main protocol
_MPS_HOME_XPATH = '//div[@class="matches_player_statistic"]//table'
_MPS_GUEST_XPATH = '//div[@class="matches_player_statistic"]//dl//table[@class="matches_penalty"]'

MATCH_REPORT_DICT = {
    'match_num': '//div[@class="games_title"]//p', #номер матча
    'match_date': '//div[@class="games_title"]//p', #дата матча
    'match_count': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="main_column"]/p[@class="count"]/span/text()',
    'match_detail_count': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="main_column"]/div[@class="detail_count"]/text()',
    'match_judges': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="main_column"]/p[2]',
    'match_line_judges': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="main_column"]/p[3]',
    'match_spectators': '//div[@class="games_title"]//p[@class="games_title_more"]',
    'home_team': _MMP_XPATH+'[1]/tr[@class="first_row"]/td[@class="first_column"]/h2',
    'home_team_region': _MMP_XPATH+'[1]/tr[@class="first_row"]/td[@class="first_column"]/p/strong',
    'home_team_coach': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="first_column"]/p/text()',
    'home_keepers': _MPS_HOME_XPATH+'[1]',
    'home_defenders': _MPS_HOME_XPATH+'[2]',
    'home_offenders': _MPS_HOME_XPATH+'[3]',
    'guest_team': _MMP_XPATH+'[1]/tr[@class="first_row"]/td[@class="right_column"]/h2',
    'guest_team_region': _MMP_XPATH+'[1]/tr[@class="first_row"]/td[@class="right_column"]/p/strong',
    'guest_team_coach': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="right_column"]/p/text()',
    'guest_keepers': _MPS_GUEST_XPATH+'[1]',
    'guest_defenders': _MPS_GUEST_XPATH+'[2]',
    'guest_offenders': _MPS_GUEST_XPATH+'[3]',
    'goals_history': '//table[@class="matches_goals"]',
    'penalties_history': '//table[@class="matches_penalty"]',
}
#----------


#PLAYER INFO
PLAYER_URL = KHL_SITE_URL+'/players/'
PLAYER_XPATH = '//div[@class="borderdiv"]/table/tbody'
PLAYER_DATA_DICT = {
    'ru_fio': '/tr[@valign="top"]/td[@valign="top"]/div[@class="big_letter"]/h2/text()',
    'en_fio': '/tr[@valign="top"]/td[@valign="top"]/div[@class="big_letter"]/h2/text()[preceding-sibling::br]',
    'photo': '/tr[@valign="top"]/td[@rowspan="3"]/div',
    'stats': '/tr[2]/td[@valign="top"]/ul/li',
    'birth_date': '/tr[2]/td[@valign="top"]/ul/li[8]/b/text()',
    'weight': '/tr[2]/td[@valign="top"]/ul/li[7]/b/text()',
    'height': '/tr[2]/td[@valign="top"]/ul/li[6]/b/text()',
    'line': '/tr[2]/td[@valign="top"]/ul/li[5]/b/text()',
    'grip': '/tr[2]/td[@valign="top"]/ul/li[9]/b/text()',
}

MD = {
        b'январь': '01',
        b'февраль': '02',
        b'март': '03',
        b'апрель': '04',
        b'маь': '05',
        b'июнь': '06',
        b'июль': '07',
        b'август': '08',
        b'сентябрь': '09',
        b'октябрь': '10',
        b'ноябрь': '11',
        b'декабрь': '12',
}

MDP = {
        b'января': '01',
        b'февраля': '02',
        b'марта': '03',
        b'апреля': '04',
        b'мая': '05',
        b'июня': '06',
        b'июля': '07',
        b'августа': '08',
        b'сентября': '09',
        b'октября': '10',
        b'ноября': '11',
        b'декабря': '12',
}

#CLUB INFO
KHL_CLUB_URL = KHL_SITE_URL+'/clubs/'
CLUB_LIST_XPATH = '//div[@class="teams"]//div[@class="team"]//div[@class="icon"]//a/@href'
CLUB_INFO_XPATH = '//div[@id="wrapper"]//div[@id="content"]'
CLUB_DATA_XPATH_DICT = {
    'logo_url': '//div[@class="clubBlock"]//img[1]/@src',
    'ru_title': '//div[@class="clubBlock"]//div[@class="info"]//div[@class="header"]/h2/text()',
    'site': '//div[@class="clubBlock"]//div[@class="info"]//table/tr[1]/td[2]/a[1]/@href',
    'opening_dt': '//div[@class="clubBlock"]//div[@class="info"]//table/tr[2]/td[1]/text()',
    'coach': '//div[@class="clubBlock"]//div[@class="info"]//table/tr[2]/td[2]/text()',
    'contacts': '//div[@class="clubTextBlock"][2]//p',
}

ARENA_DATA_XPATH_DICT = {
    'photo_url': '//div[@class="clubPhoto"]//img/@src',
    'ru_title': '/div[@class="header"]/h2/text()',
    'capacity': '//p[1]/text()',
    'site': '//p[2]//a/@href',
    'tickets_url': '//p[3]//a/@href',
    'contacts': '//p[4]',
    'contacts_alt': '//p[3]', 
}