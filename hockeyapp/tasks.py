#coding: utf-8
from __future__ import unicode_literals, print_function
import logging
#import time
import sys

#from celery.task import periodic_task
#from celery.schedules import crontab

from sportomatics.celery import app

from base.utils import str2int_safe, str2sec_safe, str2float_safe

from . import parsers
from . import models

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


@app.task(ignore_result=True, track_started=True)
def async_hockey_player_update(id):
    b'''
        Обновление инфо о игроке
    '''
    try:
        models.Player.objects.get_or_create_player(khl_id=id, update=True)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def async_temp_match_update(match_id):
    b'''
        Обновление инфо о матче в дб
    '''
    try:
        match = models.Match.objects.get(id=match_id)
        if not match.spectators and match.spectators_str:
            match.spectators = str2int_safe(match.spectators_str.strip(
                                                            ).split()[0]
            )
            match.save(update_fields=('spectators',))
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def async_temp_stats_plr_update(id):
    b'''
        Обновление инфо о статистике игрока
    '''
    try:
        obj = models.ClubPlayerMatch.objects.get(id=id)
        for field in ('plus_minus', 'penalty_time', 'ev_goals', 'pp_goals', 
        'es_goals', 'overtime_goals', 'win_goals', 'bullet_goals', 'shots',
        'faceoff', 'winfaceoff', 'loose_goals', 'saves',):
            value = str2int_safe(getattr(obj,field+'_str'))
            setattr(obj, field, value)
        for field in ('saves_p', 'pis', 'winfaceoff_p', 'saves_p', 'sf'):
            value = str2float_safe(getattr(obj,field+'_str'))
            setattr(obj, field, value)
        for field in ('gamingtime',):
            value = str2sec_safe(getattr(obj,field+'_str'))
            setattr(obj, field, value)
        obj.save()
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())