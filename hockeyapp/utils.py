#coding: utf-8
from __future__ import unicode_literals
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
            delete_duplicates(_qs, _model)
        for _model in _hg_models:
            _model.objects.filter(home_team__pk__in=dup_club_ids
                         ).update(home_team_id=club_id)
            _qs = _model.objects.filter(home_team_id=club_id)
            #delete_duplicates(_qs)
            _model.objects.filter(guest_team__pk__in=dup_club_ids
                         ).update(guest_team_id=club_id)
            _qs = _model.objects.filter(guest_team_id=club_id)
            #delete_duplicates(_qs)


def delete_duplicates(qs, model=None, exclude_field=None):
    _rows = qs.values()
    CPM = get_model(CURRENT_APP, 'ClubPlayerMatch')
    CP = get_model(CURRENT_APP, 'ClubPlayer')
    for row in _rows:
        row.pop('id', None)
        if exclude_field:
            row.pop(exclude_field, None)
        _vals = qs.filter(**row)
        if _vals.count() > 1:
            _ids = set(_vals.values_list('pk', flat=True))
            cur_id = _ids.pop()
            if model == CP:
                _cur_cp = CP.objects.get(pk=cur_id)
                _cp_qs = CP.objects.filter(pk__in=_ids)
                _cpm_qs = CPM.objects.filter(clubplayer__in=_ids)
                for _cp in _cp_qs:
                    _cur_cp.homematches.add(*_cp.homematches.all())
                    _cur_cp.guestmatches.add(*_cp.guestmatches.all())
                _cpm_qs.update(clubplayer_id=cur_id)
                _qs = CPM.objects.filter(clubplayer_id=cur_id)
                delete_duplicates(_qs)
            qs.filter(pk__in=_ids).delete()



def delete_club_players_duplicates():
    CP = get_model(CURRENT_APP, 'ClubPlayer')
    qs = CP.objects.all()
    _rows = qs.values()
    CPM = get_model(CURRENT_APP, 'ClubPlayerMatch')
    for row in _rows:
        row.pop('id', None)
        _vals = qs.filter(**row)
        if _vals.count() > 1:
            _ids = set(_vals.values_list('pk', flat=True))
            cur_id = _ids.pop()
            _cur_cp = CP.objects.get(pk=cur_id)
            _cp_qs = CP.objects.filter(pk__in=_ids)
            _cpm_qs = CPM.objects.filter(clubplayer__in=_ids)
            for _cp in _cp_qs:
                _cur_cp.homematches.add(*_cp.homematches.all())
                _cur_cp.guestmatches.add(*_cp.guestmatches.all())
            _cpm_qs.update(clubplayer_id=cur_id)
            _qs = CPM.objects.filter(clubplayer_id=cur_id)
            delete_duplicates(_qs, exclude_field='adv_stats_id')
            qs.filter(pk__in=_ids).delete()


def delete_cpm_duplicates():
    CPM = get_model(CURRENT_APP, 'ClubPlayerMatch')
    _qs = CPM.objects.all()
    delete_duplicates(_qs, exclude_field='adv_stats_id')


def create_superhigh_schedule():
    b''' Создаем расписание для superliga и Высшей лиги '''
    MM = get_model(CURRENT_APP, 'Match')
    SM = get_model(CURRENT_APP, 'Schedule')
    LM = get_model(CURRENT_APP, 'League')
    SeasonM = get_model('base', 'Season')
    dt = {
        'superleague': {
            'self': LM.objects.filter(en_title='Superliga').last(),
            'comp': (
                {
                    'start_date': datetime.datetime(day=10, month=9, year=1996),
                    'end_date': datetime.datetime(day=13, month=3, year=1997),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=15, month=3, year=1997),
                    'end_date': datetime.datetime(day=9, month=4, year=1997),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=3, month=9, year=1997),
                    'end_date': datetime.datetime(day=29, month=3, year=1998),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=1, month=4, year=1998),
                    'end_date': datetime.datetime(day=24, month=4, year=1998),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=12, month=9, year=1998),
                    'end_date': datetime.datetime(day=8, month=3, year=1999),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=11, month=3, year=1999),
                    'end_date': datetime.datetime(day=15, month=4, year=1999),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=12, month=9, year=1998),
                    'end_date': datetime.datetime(day=8, month=3, year=1999),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=11, month=3, year=1999),
                    'end_date': datetime.datetime(day=15, month=4, year=1999),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=8, month=9, year=1999),
                    'end_date': datetime.datetime(day=26, month=2, year=2000),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=29, month=2, year=2000),
                    'end_date': datetime.datetime(day=2, month=4, year=2000),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=7, month=9, year=2000),
                    'end_date': datetime.datetime(day=10, month=3, year=2001),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=11, month=3, year=2001),
                    'end_date': datetime.datetime(day=6, month=4, year=2001),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=12, month=9, year=2001),
                    'end_date': datetime.datetime(day=12, month=3, year=2002),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=15, month=3, year=2002),
                    'end_date': datetime.datetime(day=7, month=4, year=2002),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=12, month=9, year=2002),
                    'end_date': datetime.datetime(day=12, month=3, year=2003),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=15, month=3, year=2003),
                    'end_date': datetime.datetime(day=7, month=4, year=2003),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=11, month=9, year=2003),
                    'end_date': datetime.datetime(day=15, month=3, year=2004),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=18, month=3, year=2004),
                    'end_date': datetime.datetime(day=10, month=4, year=2004),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=1, month=9, year=2004),
                    'end_date': datetime.datetime(day=15, month=3, year=2005),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=18, month=3, year=2005),
                    'end_date': datetime.datetime(day=8, month=4, year=2005),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=7, month=9, year=2005),
                    'end_date': datetime.datetime(day=10, month=3, year=2006),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=13, month=3, year=2006),
                    'end_date': datetime.datetime(day=16, month=4, year=2006),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=7, month=9, year=2006),
                    'end_date': datetime.datetime(day=8, month=3, year=2007),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=11, month=3, year=2007),
                    'end_date': datetime.datetime(day=13, month=4, year=2007),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=4, month=9, year=2007),
                    'end_date': datetime.datetime(day=1, month=3, year=2008),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=4, month=3, year=2008),
                    'end_date': datetime.datetime(day=11, month=4, year=2008),
                    'type': 2,
                },
            ),
        },
        'highleague': {
            'self': LM.objects.filter(en_title='VHL-2').last(),
            'comp': (
                {
                    'start_date': datetime.datetime(day=14, month=9, year=1996),
                    'end_date': datetime.datetime(day=9, month=3, year=1997),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=17, month=9, year=1997),
                    'end_date': datetime.datetime(day=15, month=3, year=1998),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=13, month=9, year=1998),
                    'end_date': datetime.datetime(day=3, month=4, year=1999),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=11, month=9, year=1999),
                    'end_date': datetime.datetime(day=12, month=3, year=2000),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=8, month=9, year=2000),
                    'end_date': datetime.datetime(day=7, month=4, year=2001),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=15, month=9, year=2001),
                    'end_date': datetime.datetime(day=22, month=4, year=2002),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=14, month=9, year=2002),
                    'end_date': datetime.datetime(day=28, month=2, year=2003),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=1, month=3, year=2003),
                    'end_date': datetime.datetime(day=27, month=4, year=2003),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=13, month=9, year=2003),
                    'end_date': datetime.datetime(day=6, month=3, year=2004),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=7, month=3, year=2004),
                    'end_date': datetime.datetime(day=22, month=4, year=2004),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=20, month=9, year=2004),
                    'end_date': datetime.datetime(day=22, month=4, year=2005),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=20, month=9, year=2005),
                    'end_date': datetime.datetime(day=30, month=4, year=2006),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=16, month=9, year=2006),
                    'end_date': datetime.datetime(day=22, month=4, year=2007),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=15, month=9, year=2007),
                    'end_date': datetime.datetime(day=13, month=3, year=2008),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=14, month=3, year=2008),
                    'end_date': datetime.datetime(day=24, month=4, year=2008),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=13, month=9, year=2008),
                    'end_date': datetime.datetime(day=4, month=3, year=2009),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=5, month=3, year=2009),
                    'end_date': datetime.datetime(day=26, month=4, year=2009),
                    'type': 2,
                },
                {
                    'start_date': datetime.datetime(day=12, month=9, year=2009),
                    'end_date': datetime.datetime(day=4, month=3, year=2010),
                    'type': 1,
                },
                {
                    'start_date': datetime.datetime(day=5, month=3, year=2010),
                    'end_date': datetime.datetime(day=27, month=4, year=2010),
                    'type': 2,
                },
            ),
        }
    }
    matches = MM.objects.filter(schedule__isnull=True,
                        date__lte=datetime.datetime(day=30, month=6, year=2010))
    for league_data in dt.values():
        league = league_data['self']
        for  s in league_data['comp']:
            season = SeasonM.objects.get_season_by_date(s['start_date'])
            _ms = matches.filter(date__gte=s['start_date'],
                                date__lte=s['end_date'],
                                home_team__leagueclub__season=season,
                                guest_team__leagueclub__season=season,
                                home_team__leagueclub__league=league,
                                guest_team__leagueclub__league=league,
            )
            _m_ids = set(_ms.values_list('pk', flat=True))
            _ms = matches.filter(pk__in=_m_ids)
            for match in _ms:
                #h = match.home_team.leagueclub_set.filter(season=season,
                                                          #league=league).last()
                #g = match.guest_team.leagueclub_set.filter(season=season,
                                                          #league=league).last()
                #if h.league == g.league and h.league == league:
                data = dict(title=match.title,
                            league=league,
                            season=season,
                            home_team=match.home_team,
                            guest_team=match.guest_team,
                            challenge_type=s['type'],
                            match=match,
                            khl_id=match.khl_id,
                            processed=True,
                            date=match.date
                )
                schedule = SM.objects.filter(khl_id=match.khl_id).last()
                if schedule:
                    print('munch munch... strange food-->>', match.pk, schedule.pk)
                else:
                    SM.objects.get_or_create(**data)