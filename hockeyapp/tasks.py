#coding: utf-8
from __future__ import unicode_literals

#from celery.task import periodic_task
#from celery.schedules import crontab

from sportomatics.celery import app

from .parsers import HockeyMatchParser


@app.task(ignore_result=True)
def async_hockey_match_parser(matchid):
    b'''
        Основная celery функция проверки пользователей.
    '''
    HockeyMatchParser().put_data_in_db_from_page(matchid)