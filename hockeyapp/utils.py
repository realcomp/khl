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


def get_arena_instagram_locations():
    ''' get instagram arena location values by latitude and longittude '''
    _model = get_model(CURRENT_APP, 'Arena')
    arenas = _model.objects.filter(coords__isnull=False
                         ).exclude(coords='')
    _model = get_model(CURRENT_APP, 'ArenaInstagram')
    arena_instagram_creator = _model.objects.get_or_create
    for arena in arenas:
        lat, lng = arena.coords.split(',')
        data = insta_api.location_search(lat=lat, lng=lng)
        for l in data:
            arena_instagram_creator(im_id=l.id, name=l.name, arena=arena,
                                    lat=l.point.latitude, 
                                    lng=l.point.longitude
            )

def _get_pictures(insta_loc_id, club, max_id=None):
    _ts_min = 1388520000
    _fn = club.image_folder_name
    data, next = insta_api.location_recent_media(location_id=insta_loc_id,
                                                min_timestamp=_ts_min,
                                                max_id=max_id)
    if data:
        for item in data:
            if item.type == 'image':
                iif = InstagramImageFile.objects.get_or_create_iif(item, _fn)
                _cpm = get_model(CURRENT_APP, 'ClubPhotos')
                _cpm.objects.get_or_create(club=club, photo=iif)
    if next:
        max_id = re.search('max_id=(\d+)', next).group(0).split('=')[1]
        _get_pictures(insta_loc_id, club, max_id)


def get_instagram_pictures():
    ''' get instagram pictures by location_id '''
    _model = get_model(CURRENT_APP, 'Club')
    clubs = _model.objects.filter(arena__isnull=False)
    for club in clubs:
        if club.arena.arenainstagram_set.exists():
            caims = club.arena.arenainstagram_set.all()
            for obj in caims:
                _get_pictures(obj.im_id, club)