#coding: utf-8
from __future__ import print_function, unicode_literals

__author__='smirnov.ev'

from ..defaults import DEFAULT_KHL_CLUB_URL, CLUB_LIST_XPATH

from . import GrabParser


class GetAllClubURLs(GrabParser):
    url = DEFAULT_KHL_CLUB_URL
    absolute_url = url
    as_get_param = False

    def get_page(self, id=None):
        b'''  смотрим список игроков '''
        self.page_tree = super(GetAllClubURLs, self).get_page()
        if self.page_tree is not None:
            return self.page_tree.xpath(CLUB_LIST_XPATH)