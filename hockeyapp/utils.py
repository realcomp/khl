import datetime
import json
import re

from django.conf import settings
from django.db.models.loading import get_model
from django.utils import timezone

from instagram.client import InstagramAPI

from base.models import InstagramImageFile


CURRENT_APP = __package__.split('.')[0]


def get_season_start_date(year=None):
    '''
    Return season start date (july 1) in chosen year
    '''
    MONTH = 7
    DAY = 1
    if not year:
        # get current season
        now = datetime.datetime.now().date()
        year = now.year
        start = datetime.date(year=year, month=MONTH, day=DAY)
        if now >= start:  # season already started in current year
            return start
        else:  # so should be previous year then
            return datetime.date(year=year - 1, month=MONTH, day=DAY)
    return datetime.date(year=year, month=MONTH, day=DAY)


def get_season_end_date(year=None):
    '''
    Return season start date (june 30) in chosen year
    '''
    MONTH = 6
    DAY = 30
    if not year:
        # get current season
        now = datetime.datetime.now().date()
        year = now.year
        end = datetime.date(year=year, month=MONTH, day=DAY)
        if now <= end:  # season not ended yet in current year
            return end
        else:  # so should be next year then
            return datetime.date(year=year + 1, month=MONTH, day=DAY)
    return datetime.date(year=year, month=MONTH, day=DAY)


def khl_string_data2python_obj_safe(string):
    try:
        string = string.split('\n')[1].split(' = ')[1][:-1]
        if string[-2] == ',':
            string = string[:-2]+string[-1]
        return json.loads(string)
    except:
        return None


def month_range(datetime_start, datetime_end):
    '''
    Split datetime interval by month
    '''
    d = timezone.datetime(
        year=datetime_start.year, month=datetime_start.month, day=1,
        tzinfo=datetime_start.tzinfo)
    while d < datetime_end:
        month = d.month + 1
        year = d.year
        if month == 13:
            month = 1
            year += 1
        yield d
        d = timezone.datetime(
            year=year, month=month, day=1, tzinfo=datetime_start.tzinfo)
    yield datetime_end


insta_api = InstagramAPI(client_id=settings.INSTAGRAM_ID,
                         client_secret=settings.INSTAGRAM_SECRET)


def get_arena_instagram_locations(coords):
    ''' get instagram arena location values by latitude and longittude '''
    lat, lng = coords.split(',')
    data = insta_api.location_search(lat=lat, lng=lng)
    return set([l.id for l in data])