#coding: utf-8
from __future__ import print_function, unicode_literals

__author__='smirnov.ev'
import datetime

from django.db.models.loading import get_model

from .. import defaults

from . import GrabParser

CURRENT_APP = __package__.split('.')[0]


class GetAllClubURLs(GrabParser):
    url = defaults.KHL_CLUB_URL
    absolute_url = url
    as_get_param = False

    def get_page(self, id=None):
        b''' список URL клубов '''
        self.page_tree = super(GetAllClubURLs, self).get_page()
        if self.page_tree is not None:
            return self.page_tree.xpath(defaults.CLUB_LIST_XPATH)


class ArenaInfo(GrabParser):
    url = defaults.KHL_SITE_URL
    absolute_url = url
    as_get_param = False
    body_xpath = defaults.CLUB_INFO_XPATH
    xpath_dict = defaults.ARENA_DATA_XPATH_DICT

    def get_page(self, id=None):
        b''' Страница информации о клубе '''
        self.page_tree = super(ArenaInfo, self).get_page(id)
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
        return self._get_strip_value('capacity').split(':')[1].strip()


class ClubInfo(GrabParser):
    url = defaults.KHL_SITE_URL
    absolute_url = url
    as_get_param = False
    body_xpath = defaults.CLUB_INFO_XPATH
    xpath_dict = defaults.CLUB_DATA_XPATH_DICT
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
        self.page_tree = super(ClubInfo, self).get_page(id)
        if self.page_tree is not None:
            _html_body = self.g.response.unicode_body()
            return self.get_club_data(html_body=_html_body)

    def get_club_data(self, html_body=None):
        b'''
            Данные o клубе через DOM-дерево
        '''
        if self.page_tree is not None:
            return {
                    'url': self.absolute_url,
                    'html_body': self.get_html_body(html_body),
                    'ru_title': self.get_ru_title(),
                    'site': self.get_site_url(),
                    'logo_url': self.get_logo_url(),
                    'opening_dt': self.get_opening_dt(),
                    'coach': self.get_coach(),
                    'contacts': self.get_contacts(),
                    'arena': self.get_arena_info()
            }

    def get_arena_info(self):
        b''' Информация о арене '''
        url = self.absolute_url+'arena/'
        return ArenaInfo(absolute_url=url).get_page()

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
        return self._get_strip_value('coach')

    def get_contacts(self):
        b''' Контакты клуба '''
        return self._get_value('contacts')[0].text_content()

    def get_logo_url(self):
        b''' URL логотипа клуба '''
        return self.url+self._get_strip_value('logo_url')