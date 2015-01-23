#coding: utf-8
from __future__ import unicode_literals


# KHL MATCH ####################################################################
KHL_SITE_URL =  'http://www.khl.ru'
KHL_MATCH_URL = KHL_SITE_URL+'/game/266/'
KHL_MATCH_PROTOCOL_XPATH = '//div[@id="wrapper"]/div[@id="content"]'
KHL_BODY_NOTEXISTS = b'Протокол не найден'
KHL_BODY_NOTEXISTS_ALT = b'Не найден протокол игры'
KHL_EMPTY_PAGE_TEXT = 'Fatal error'
KHL_MATCH_REPORT_DICT = {
    'match_num': '//div[@class="header"]/h2/text()', #номер матча
    'match_date':  '//div[@class="header"]/h2/text()', #дата матча
    'match_count': '/div[@class="gameHeader"]/div[@class="time"]/div[@class="time-preview"]/div[@class="counter"]/b/text()',
    'match_detail_count': '/div[@class="gameHeader"]/div[@class="time"]/div[@class="time-preview"]/div[2]/text()',
    'match_judges': '/div[@class="gameHeader"]/table[@class="info"]/tr[2]/td[2]/text()',
    'match_line_judges': '/div[@class="gameHeader"]/table[@class="info"]/tr[3]/td[2]/text()',
    'match_spectators': '/div[@class="gameHeader"]/table[@class="info"]/tr[1]/td[2]/text()',
    'home_team': '/div[@class="gameHeader"]/div[@class="teamName left"]/div[@class="name"]/text()',
    'home_team_region': '/div[@class="gameHeader"]/div[@class="teamName left"]/div[@class="name"]/span[1]/text()',
    'home_team_coach': '/div[@class="gameHeader"]/div[@class="teamName left"]/div[@class="name"]/span[@class="trainer"]/text()',
    'home_keepers': '/div[@class="gameTabs"]/div[@class="section"]/script[1]/text()',
    'home_defenders': '/div[@class="gameTabs"]/div[@class="section"]/script[2]/text()',
    'home_offenders': '/div[@class="gameTabs"]/div[@class="section"]/script[3]/text()',
    'guest_team': '/div[@class="gameHeader"]/div[@class="teamName"]/div[@class="name"]/text()',
    'guest_team_region': '/div[@class="gameHeader"]/div[@class="teamName"]/div[@class="name"]/span[1]/text()',
    'guest_team_coach': '/div[@class="gameHeader"]/div[@class="teamName"]/div[@class="name"]/span[@class="trainer"]/text()',
    'guest_keepers': '/div[@class="gameTabs"]/div[@class="section"]/script[4]/text()',
    'guest_defenders': '/div[@class="gameTabs"]/div[@class="section"]/script[5]/text()',
    'guest_offenders': '/div[@class="gameTabs"]/div[@class="section"]/script[6]/text()',
    'goals_history': '/div[@class="gameTabs"]/script/text()',
    'penalties_history': '/div[@class="gameTabs"]/div[@class="section"]/div[@class="dataTables_wrapper"]/table[@class="dataTable stripe compact row-border hl no-footer"]',
}
################################################################################


# MHL MATCH ####################################################################
MHL_BODY_NOTEXISTS = b'Протокол не найден'
MHL_BODY_NOTEXISTS_ALT = b'Не найден протокол игры'
MHL_EMPTY_PAGE_TEXT = 'Fatal error'
MHL_MATCH_PROTOCOL_XPATH = '//div[@class="content"]//div[@class="b-left"]//div[@class="second_content"]'
MHL_URL = 'http://mhl.khl.ru/report/272/'
MHL_BODY_XPATH = MHL_MATCH_PROTOCOL_XPATH+'//div[@class="inner_content"]'
_MMP_XPATH = '//table[@class="matches_protocol_main"]' #xpath match main protocol
_MPS_HOME_XPATH = '//div[@class="matches_player_statistic"]//table'
_MPS_GUEST_XPATH = '//div[@class="matches_player_statistic"]//dl//table[@class="matches_penalty"]'
MHL_MATCH_REPORT_DICT = {
    'match_num': '//div[@class="games_title"]/p/text()', #номер матча
    'match_date': '//div[@class="games_title"]/p/text()', #дата матча
    'match_count': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="main_column"]/p[@class="count"]/span/text()',
    'match_detail_count': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="main_column"]/div[@class="detail_count"]/text()',
    'match_judges': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="main_column"]/p[2]',
    'match_line_judges': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="main_column"]/p[3]',
    'match_spectators': '//div[@class="games_title"]//p[@class="games_title_more"]/text()',
    'home_team': _MMP_XPATH+'[1]/tr[@class="first_row"]/td[@class="first_column"]/h2/text()',
    'home_team_region': _MMP_XPATH+'[1]/tr[@class="first_row"]/td[@class="first_column"]/p/strong/text()',
    'home_team_coach': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="first_column"]/p/text()',
    'home_keepers': _MPS_HOME_XPATH+'[1]',
    'home_defenders': _MPS_HOME_XPATH+'[2]',
    'home_offenders': _MPS_HOME_XPATH+'[3]',
    'guest_team': _MMP_XPATH+'[1]/tr[@class="first_row"]/td[@class="right_column"]/h2/text()',
    'guest_team_region': _MMP_XPATH+'[1]/tr[@class="first_row"]/td[@class="right_column"]/p/strong/text()',
    'guest_team_coach': _MMP_XPATH+'[2]/tr[@class="second_row"]/td[@class="right_column"]/p/text()',
    'guest_keepers': _MPS_GUEST_XPATH+'[1]',
    'guest_defenders': _MPS_GUEST_XPATH+'[2]',
    'guest_offenders': _MPS_GUEST_XPATH+'[3]',
    'goals_history': '//table[@class="matches_goals"]',
    'penalties_history': '//table[@class="matches_penalty"]',
}
################################################################################


# VHL MATCH ####################################################################
VHL_SITE_URL =  'http://www.vhlru.ru'
VHL_MATCH_URL = VHL_SITE_URL+'/report/269/'
VHL_MATCH_PROTOCOL_XPATH = '//div[@id="page_wrap"]/div[@class="center"]/div[@id="content"]/div[@class="lcol"]'
VHL_BODY_NOTEXISTS = b'Протокол не найден'
VHL_BODY_NOTEXISTS_ALT = b'Не найден протокол игры'
VHL_EMPTY_PAGE_TEXT = 'Fatal error'
_MMP_XPATH = '/table[@class="matches_protocol_main"]' #xpath match main protocol
_MPS_HOME_XPATH = '/div[@class="matches_player_statistic"]/table'
_MPS_GUEST_XPATH = '/div[@class="matches_player_statistic"]/dl/table[@class="tablesorter matches_penalty"]'
VHL_MATCH_REPORT_DICT = {
    'match_num': '//div[@class="games_title"]/p/text()', #номер матча
    'match_date': '//div[@class="games_title"]/p/text()', #дата матча
    'match_count': _MMP_XPATH+'/tr[@class="first_row"]/td[@class="main_column"]/p[@class="count"]/span/text()',
    'match_detail_count': _MMP_XPATH+'/tr[@class="first_row"]/td[@class="main_column"]/div[@class="detail_count"]/text()',
    'match_judges': _MMP_XPATH+'/tr[2]/td[@class="treners"][2]/p',
    'match_line_judges': _MMP_XPATH+'/tr[2]/td[@class="treners"][2]',
    'match_spectators': '//div[@class="games_title"]//p[@class="games_title_more"]/text()',
    'home_team': _MMP_XPATH+'/tr[@class="first_row"]/td[1]/a/text()',
    'home_team_region': _MMP_XPATH+'/tr[@class="first_row"]/td[1]/div/strong/text()',
    'home_team_coach': _MMP_XPATH+'/tr[2]/td[@class="treners"][1]',
    'home_keepers': _MPS_HOME_XPATH+'[1]',
    'home_defenders': _MPS_HOME_XPATH+'[2]',
    'home_offenders': _MPS_HOME_XPATH+'[3]',
    'guest_team': _MMP_XPATH+'/tr[@class="first_row"]/td[3]/a/text()',
    'guest_team_region': _MMP_XPATH+'/tr[@class="first_row"]/td[3]/div/strong/text()',
    'guest_team_coach': _MMP_XPATH+'/tr[2]/td[@class="treners"][3]',
    'guest_keepers': _MPS_GUEST_XPATH+'[1]',
    'guest_defenders': _MPS_GUEST_XPATH+'[2]',
    'guest_offenders': _MPS_GUEST_XPATH+'[3]',
    'goals_history': '/table[@class="tablesorter matches_goals"]',
    'penalties_history': '/table[@class="tablesorter matches_penalty"]',
}
################################################################################

#KHL Match Advanced DATA INFO
MATCH_ADV_STATS_URL = 'http://text.khl.ru/text/'
MATCH_ADV_STATS_XPATH = '//div[@id="wrapper"]/div[@class="grey-block"]/div[@class="tabs-block"]'
MATCH_ADV_STATC_DICT = {
    'home_team': {
                    'shots': '/div[@class="box"][2]/table/tr/td[1]/table/tr[@class]',
                    'faceoff': '/div[@class="box"][3]/table/tr/td[1]/table/tr[@class]',
                    'gamingtime': '/div[@class="box"][4]/table/tr/td[1]/table//tbody/tr[@class]',
                    'extra': '/div[@class="box"][6]/table/tr/td[1]/table/tbody/tr',

    },
    'guest_team': {
                    'shots': '/div[@class="box"][2]/table/tr/td[3]/table/tr[@class]',
                    'faceoff': '/div[@class="box"][3]/table/tr/td[3]/table/tr[@class]',
                    'gamingtime': '/div[@class="box"][4]/table/tr/td[3]/table/tbody/tr[@class]',
                    'extra': '/div[@class="box"][6]/table/tr/td[2]/table/tbody/tr',
    }
}
MATCH_PLAYER_SHOTS = {
                    'shots_1th': 'td[2]', #/text()',
                    'shots_2nd': 'td[3]', #/text()',
                    'shots_3th': 'td[4]', #/text()',
                    'shots_all': 'td[5]', #/text()',
}
MATCH_PLAYER_FACEOFFS = {
                    'faceoff_1th': 'td[2]/text()',
                    'faceoff_2nd': 'td[3]/text()',
                    'faceoff_3th': 'td[4]/text()',
                    'faceoff_all': 'td[5]/text()',
}
MATCH_PLAYER_GAMINGTIMES = {
                    'change_count_1th': 'td[2]/text()',
                    'gamingtime_1th': 'td[3]/text()',
                    'change_count_2nd': 'td[4]/text()',
                    'gamingtime_2nd': 'td[5]/text()',
                    'change_count_3th': 'td[6]/text()',
                    'gamingtime_3th': 'td[7]/text()',
                    'change_count_all': 'td[8]/text()',
                    'gamingtime_all': 'td[9]/text()',
}
MATCH_PLAYER_EXTRAS = {
                    'block_1th': 'td[2]/text()',
                    'hit_1th': 'td[3]/text()',
                    'foul_1th': 'td[4]/text()',
                    'block_2nd': 'td[5]/text()',
                    'hit_2nd': 'td[6]/text()',
                    'foul_2nd': 'td[7]/text()',
                    'block_3th': 'td[8]/text()',
                    'hit_3th': 'td[9]/text()',
                    'foul_3th': 'td[10]/text()',
                    'block_all': 'td[11]/text()',
                    'hit_all': 'td[12]/text()',
                    'foul_all': 'td[13]/text()',
}
#----------


#KHL PLAYER INFO
PLAYER_URL = KHL_SITE_URL+'/players/'
PLAYER_XPATH = '//div[@class="borderdiv"]/table/tbody'
PLAYER_DATA_DICT = {
    'ru_fio': '/tr[@valign="top"]/td[@valign="top"]/div[@class="big_letter"]/h2/text()',
    'en_fio': '/tr[@valign="top"]/td[@valign="top"]/div[@class="big_letter"]/h2/text()[preceding-sibling::br]',
    'photo': '/tr[@valign="top"]/td[@rowspan="3"]/div',
    'stats': '/tr[2]/td[@valign="top"]/ul/li',
    'club': '/tr[2]/td[@valign="top"]/ul/li[1]/b/text()',
    'contract_type': '/tr[2]/td[@valign="top"]/ul/li[2]/b/text()',
    'contract_to': '/tr[2]/td[@valign="top"]/ul/li[3]/b/text()',
    'number': '/tr[2]/td[@valign="top"]/ul/li[4]/b/text()',
    'line': '/tr[2]/td[@valign="top"]/ul/li[5]/b/text()',
    'height': '/tr[2]/td[@valign="top"]/ul/li[6]/b/text()',
    'weight': '/tr[2]/td[@valign="top"]/ul/li[7]/b/text()',
    'grip': '/tr[2]/td[@valign="top"]/ul/li[8]/b/text()',
    'birth_date': '/tr[2]/td[@valign="top"]/ul/li[9]/b/text()',
    'birth_date_alt': '/tr[2]/td[@valign="top"]/ul/li[4]/b/text()',
    'death_date': '/tr[2]/td[@valign="top"]/ul/li[9]/b/text()',
    'citizenship': '/tr[2]/td[@valign="top"]/ul/li[11]/b/text()',
    'all': '/tr[2]/td[@valign="top"]/ul/b/text()',
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

MD_EN = {
        b'january': '01',
        b'february': '02',
        b'march': '03',
        b'april': '04',
        b'may': '05',
        b'june': '06',
        b'july': '07',
        b'august': '08',
        b'september': '09',
        b'october': '10',
        b'november': '11',
        b'december': '12',
}

#KHL CLUB INFO
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