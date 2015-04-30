# -*- coding: utf-8 -*-
import sys

from sportomatics.celery import app

from . import logger, models


@app.task(ignore_result=True, track_started=True)
def player_recalc_counters(pks, fields, update_last_match_date=False):
    b'''
        Пересчет полей игрока на основе данных по матчам
        seasons_total
        matches_total
        goals_total
        assists_total
        points_total
        plus_minus_total
        goals_average
        assists_average
        points_average
        plus_minus_average
        ...
    '''
    try:
        models.Player.objects.filter(pk__in=pks).recalc_counters(
            fields, update_last_match_date=update_last_match_date)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def player_recalc_counters_index(field):
    b'''
        Пересчет позиции игрока в сортировке
    '''
    try:
        models.Player.objects.recalc_counters_index(field)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())
