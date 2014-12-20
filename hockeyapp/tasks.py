#coding: utf-8
from __future__ import unicode_literals, print_function
import logging
#import time
import sys

#from celery.task import periodic_task
#from celery.schedules import crontab

from sportomatics.celery import app

from . import parsers

logger = logging.getLogger('root')

@app.task(ignore_result=True, track_started=True)
def async_hockey_match_parser(matchid):
    b'''
        Парсер матча.
    '''
    try:
        parsers.match.HockeyMatchParser(html=True
            ).put_data_in_db_from_page(matchid)
        #parsers.match.HockeyMatchParser(html=False).get_page(matchid)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def async_hockey_matches_parser(id, matches):
    b'''
        Парсер матчей.
        Требует два аргумента:
            1. стартовый id матча
            2. Счетчик количества id
    '''
    for i in range(matches):
        matchid = id+i
        try:
            async_hockey_match_parser.delay(matchid)
        except Exception, exc:
            logger.error(exc, exc_info=sys.exc_info())
        #if i%100 == 0:
        #time.sleep(10)