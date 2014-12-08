#coding: utf-8
from __future__ import unicode_literals


DEFAULT_KHL_MATCH_PROTOCOL_XPATH = '//div[@class="content"]//div[@class="b-left"]//div[@class="second_content"]'
DEFAULT_EMPTY_PAGE_TEXT = 'Fatal error'
DEFAULT_BODY_NOTEXISTS = b'Протокол не найден'
DEFAULT_BODY_XPATH = DEFAULT_KHL_MATCH_PROTOCOL_XPATH+'//div[@class="inner_content"]'
#DEFAULT_MATCH_MAIN_PROTOCOL_XPATH = DEFAULT_BODY_XPATH+'//table[@class="matches_protocol_main"]'