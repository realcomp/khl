#coding: utf-8
from __future__ import print_function, unicode_literals

__author__='smirnov.ev'
import datetime

from django.db.models.loading import get_model

from base.utils import str2int_safe

from . import GrabParser
from . import xpathes


CURRENT_APP = __package__.split('.')[0]


class KHLClubURLs(GrabParser):
    b''' URL клубов с сайта КХЛ '''
    url = xpathes.KHL_CLUB_URL
    absolute_url = url
    as_get_param = False

    def get_page(self, id=None):
        b''' список URL клубов '''
        self.page_tree = super(KHLClubURLs, self).get_page()
        if self.page_tree is not None:
            return self.page_tree.xpath(xpathes.KHL_CLUB_LIST_XPATH)


class KHLArenaInfo(GrabParser):
    b''' инфо о арене с сайта КХЛ '''
    url = xpathes.KHL_SITE_URL
    absolute_url = url
    as_get_param = False
    body_xpath = xpathes.KHL_CLUB_INFO_XPATH
    xpath_dict = xpathes.KHL_ARENA_XPATH_DICT

    def get_page(self, id=None):
        b''' Страница информации о клубе '''
        self.page_tree = super(KHLArenaInfo, self).get_page(id)
        if self.page_tree is not None:
            return self.get_arena_data()

    def get_arena_data(self, html_body=None):
        b'''
            Данные oб арене клуба через DOM-дерево
        '''
        if self.page_tree is not None:
            return {
                    'ru_title': self.get_ru_title(),
                    'site': self.get_site_url(),
                    'photo_url': self.get_photo_url(),
                    'contacts': self.get_contacts(),
                    'capacity': self.get_capacity(),
                    'tickets_url': self.get_tickets_url(),
            }

    def get_ru_title(self):
        b''' Название арены клуба '''
        return self._get_strip_value('ru_title')

    def get_site_url(self):
        b''' URL сайта арены клуба '''
        return self._get_strip_value('site')

    def get_tickets_url(self):
        b''' URL сайта продажи билетов клуба '''
        return self._get_strip_value('tickets_url')

    def get_photo_url(self):
        b''' URL фото арены клуба '''
        return self.url+self._get_strip_value('photo_url')

    def get_contacts(self):
        b''' Контактные данные арены клуба '''
        contacts = self._get_value('contacts')
        if contacts:
            return self._get_value('contacts')[0].text_content()
        else:
            return self._get_value('contacts_alt')[0].text_content()

    def get_capacity(self):
        b''' Вместимость арены клуба '''
        _value = self._get_strip_value('capacity'
                    ).split(':')[1].strip().encode('utf-8')
        return str2int_safe(_value.split(b'зрител')[0].replace(' ', ''))


class KHLClubInfo(GrabParser):
    b''' инфо о клубе с сайта КХЛ '''
    url = xpathes.KHL_SITE_URL
    absolute_url = url
    as_get_param = False
    body_xpath = xpathes.KHL_CLUB_INFO_XPATH
    xpath_dict = xpathes.KHL_CLUB_XPATH_DICT
    model_name = 'Club'

    def put_data_in_db_from_page(self, id=None):
        b'''Основной метод, берующий данные со стороннего сайта и кладущий
            в БД, если все хорошо
        ''' 
        data = self.get_page(id)
        if data and self.model_name:
            model = get_model(CURRENT_APP, self.model_name)
            return model.objects.create_or_update_club(self.absolute_url,
                                                        update=True,
                                                        data=data)

    def get_page(self, id=None):
        b''' Страница информации о клубе '''
        self.page_tree = super(KHLClubInfo, self).get_page(id)
        if self.page_tree is not None:
            _html_body = self.g.response.unicode_body()
            return self.get_club_data(html_body=_html_body, id=id)

    def get_club_data(self, html_body=None, id=None):
        b'''
            Данные o клубе через DOM-дерево
        '''
        if self.page_tree is not None:
            _res = {
                    'url': self.absolute_url,
                    'html_body': self.get_html_body(html_body),
                    'ru_title': self.get_ru_title(),
                    'site': self.get_site_url(),
                    'logo_url': self.get_logo_url(),
                    'opening_dt': self.get_opening_dt(),
                    'coach': self.get_coach(),
                    'contacts': self.get_contacts(),
                    'arena': self.get_arena_info(),
                    'players': self.get_players(id) or []
            }
            return _res

    def get_arena_info(self):
        b''' Информация о арене '''
        url = self.absolute_url+'arena/'
        return KHLArenaInfo(absolute_url=url).get_page()

    def get_ru_title(self):
        b''' Название клуба '''
        return self._get_strip_value('ru_title')

    def get_site_url(self):
        b''' URL сайта клуба '''
        return self._get_strip_value('site')

    def get_opening_dt(self):
        b''' Дата основания клуба '''
        _year = int(self._get_strip_value('opening_dt').split()[2]) 
        return datetime.datetime(day=1,month=1,year=_year)

    def get_coach(self):
        b''' Главный тренер клуба '''
        return self._get_strip_value('coach').split(':')[1]

    def get_contacts(self):
        b''' Контакты клуба '''
        return self._get_value('contacts')[0].text_content()

    def get_logo_url(self):
        b''' URL логотипа клуба '''
        return self.url+self._get_strip_value('logo_url')

    def get_players(self, id=''):
        url = self.absolute_url+'team'
        plrs_page_tree = GrabParser(absolute_url=url).get_page()
        plrs_links = plrs_page_tree.xpath(xpathes.KHL_PLAYERS_XPATH)
        if plrs_links:
            return set(link.split('/')[-2] for link in plrs_links)#khl_id set
################################################################################
################################################################################
################################################################################


class VHLClubURLs(GrabParser):
    b''' URL клубов с сайта ВХЛ '''
    url = xpathes.VHL_CLUB_URL
    absolute_url = url
    as_get_param = False

    def get_page(self, id=None):
        b''' список URL клубов '''
        self.page_tree = super(VHLClubURLs, self).get_page()
        if self.page_tree is not None:
            return set(self.page_tree.xpath(xpathes.VHL_CLUB_LIST_XPATH))


class VHLClubInfo(KHLClubInfo):
    b''' инфо о клубе с сайта ВХЛ '''
    url = xpathes.VHL_SITE_URL
    absolute_url = url
    body_xpath = xpathes.VHL_CLUB_INFO_XPATH
    xpath_dict = xpathes.VHL_CLUB_XPATH_DICT

    def get_club_data(self, html_body=None, id=None):
        b'''
            Данные o клубе через DOM-дерево
        '''
        if self.page_tree is not None:
            _res = {
                    'url': self.absolute_url,
                    'html_body': self.get_html_body(html_body),
                    'ru_title': self.get_ru_title(),
                    'site': self.get_site_url(),
                    'logo_url': self.get_logo_url(),
                    'contacts': self.get_contacts(),
                    'players': self.get_players() or []
            }
            return _res

    def get_ru_title(self):
        b''' Название клуба '''
        return self._get_strip_value('ru_title').split(':')[1].strip()

    def get_players(self, id=''):
        plrs_links = self._get_value('players')
        if plrs_links:
            return set(link.split('/')[-2] for link in plrs_links)#khl_id set
################################################################################
################################################################################
################################################################################


class MHLClubURLs(GrabParser):
    b''' URL клубов с сайта MХЛ '''
    url = xpathes.MHL_CLUB_URL
    absolute_url = url
    as_get_param = False

    def get_page(self, id=None):
        b''' список URL клубов '''
        self.page_tree = super(MHLClubURLs, self).get_page()
        if self.page_tree is not None:
            return set(self.page_tree.xpath(xpathes.MHL_CLUB_LIST_XPATH))


class MHLClubInfo(VHLClubInfo):
    b''' инфо о клубе с сайта MХЛ '''
    url = xpathes.MHL_SITE_URL
    absolute_url = url
    body_xpath = xpathes.MHL_CLUB_INFO_XPATH
    xpath_dict = xpathes.MHL_CLUB_XPATH_DICT

    def get_club_data(self, html_body=None, id=None):
        b'''
            Данные o клубе через DOM-дерево
        '''
        if self.page_tree is not None:
            _res = {
                    'url': self.absolute_url,
                    'html_body': self.get_html_body(html_body),
                    'ru_title': self.get_ru_title(),
                    'site': self.get_site_url(),
                    'logo_url': self.get_logo_url(),
                    'players': self.get_players() or []
            }
            return _res
################################################################################
################################################################################
################################################################################


class MHL2ClubURLs(GrabParser):
    b''' URL клубов с сайта MХЛ-2 '''
    url = xpathes.MHL2_CLUB_URL
    absolute_url = url
    as_get_param = False

    def get_page(self, id=None):
        b''' список URL клубов '''
        self.page_tree = super(MHL2ClubURLs, self).get_page()
        if self.page_tree is not None:
            return set(self.page_tree.xpath(xpathes.MHL2_CLUB_LIST_XPATH))


class MHL2ClubInfo(VHLClubInfo):
    b''' инфо о клубе с сайта MХЛ '''
    url = xpathes.MHL2_SITE_URL
    absolute_url = url
    body_xpath = xpathes.MHL2_CLUB_INFO_XPATH
    xpath_dict = xpathes.MHL2_CLUB_XPATH_DICT

    def _get_absolute_url(self, id=None, slash=True):
        b'''определяем url страницы
            По-умолчанию: self.absolute_url = self.url
        '''
        if id:
            _url = b'{0}{1}'.format(id,'/' if slash else '')
            self.absolute_url = b'{0}{1}'.format(xpathes.MHL2_CLUB_URL,_url)
        return self.absolute_url

    def get_club_data(self, html_body=None, id=None):
        b'''
            Данные o клубе через DOM-дерево
        '''
        if self.page_tree is not None:
            _res = {
                    'url': self.absolute_url,
                    'html_body': self.get_html_body(html_body),
                    'ru_title': self.get_ru_title(),
                    #'site': self.get_site_url(),
                    'logo_url': self.get_logo_url(),
                    'players': self.get_players() or []
            }
            return _res