import datetime
import json

from django.conf import settings
from django.db.models.loading import get_model
from django.utils import timezone

from instagram.client import InstagramAPI


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


def delete_club_duplicates_with_relation():
    _clubs = {
                10: (148,),
                12: (218,),
                13: (278,),
                20: (132,),
                26: (289,),
                29: (73,69,),
                36: (314,),
                37: (217,89,),
                52: (136,15,),
                57: (324,99,),
                58: (323,1,),
                65: (75,149,30,),
                76: (311,),
                77: (269,),
                141: (214,),
                164: (224,),
                185: (256,),
                194: (286,),
                204: (167,),
                213: (95,200,87,),
                219: (165,226,),
                257: (283,),
                264: (50,33,),
                271: (172,),
                300: (247,),
                313: (243,),
                321: (144,),
                322: (198,),
    }
    club_rel_models = (
        get_model(CURRENT_APP, 'AddressClub'),
        get_model(CURRENT_APP, 'LeagueClub'),
        get_model(CURRENT_APP, 'ClubPlayer'),
        get_model(CURRENT_APP, 'CoachClub'),
        get_model(CURRENT_APP, 'LogoClubHistory'),
        get_model(CURRENT_APP, 'ClubSocial'),
        get_model(CURRENT_APP, 'Timeline'),       
    )
    _hg_models = (
        get_model(CURRENT_APP, 'Match'),
        get_model(CURRENT_APP, 'Schedule')
    )
    for club_id, dup_club_ids in _clubs.items():
        for _model in club_rel_models:
            _model.objects.filter(club__pk__in=dup_club_ids
                          ).update(club_id=club_id)
            _qs = _model.objects.filter(club_id=club_id)
            delete_duplicates(_qs)
        for _model in _hg_models:
            _model.objects.filter(home_team__pk__in=dup_club_ids
                         ).update(home_team_id=club_id)
            _qs = _model.objects.filter(home_team_id=club_id)
            delete_duplicates(_qs)
            _model.objects.filter(guest_team__pk__in=dup_club_ids
                         ).update(guest_team_id=club_id)
            _qs = _model.objects.filter(guest_team_id=club_id)
            delete_duplicates(_qs)


def delete_duplicates(qs):
    _rows = qs.values()
    for row in _rows:
        row.pop('id', None)
        _vals = qs.filter(**row)
        if _vals.count() > 1:
            _ids = set(_vals.values_list('pk', flat=True))
            _ids.pop()
            qs.filter(pk__in=_ids).delete()
