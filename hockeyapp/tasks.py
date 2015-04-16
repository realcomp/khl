#coding: utf-8
from __future__ import unicode_literals, print_function

import datetime
import itertools
import re
import sys
import time

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from django.conf import settings

from sportomatics.celery import app

from instagram.client import InstagramAPI

from base.models import InstagramImageFile
from base.utils import str2int_safe

from . import parsers
from . import models
from . import utils
from . import timeline_tasks


@app.task(ignore_result=True, track_started=True)
def club_async_update(links, parser):
    for link in links:
        try:
            parser().put_data_in_db_from_page(link[:-1]) #remove last slash
        except Exception, exc:
            logger.error(exc, exc_info=sys.exc_info())

@app.task(ignore_result=True, track_started=True)
def periodic_update_clubs():
    try:
        for links, club_parser in ( 
            (parsers.club.KHLClubURLs().get_page(), parsers.club.KHLClubInfo), 
            (parsers.club.VHLClubURLs().get_page(), parsers.club.VHLClubInfo),
            (parsers.club.MHLClubURLs().get_page(), parsers.club.MHLClubInfo),
            (parsers.club.MHL2ClubURLs().get_page(), parsers.club.MHL2ClubInfo),
        ):
            if club_parser:
                club_async_update.delay(links, club_parser)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def periodic_update_schedules():
    try:
        for chlng in models.Challenge.objects.filter(processed=False):
            _parser = getattr(parsers.schedule, chlng.parser_type)
            _parser(absolute_url=chlng.url
                ).put_data_in_db_from_page( challenge = chlng,
                                            challenge_type=chlng.challenge_type)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def periodic_get_matches():
    try:
        matches = models.Schedule.objects.filter(khl_id__isnull=False,
                                                processed=False,
                                                challenge__isnull=False,
                                                match__isnull=True)
        for m in matches:
            async_hockey_match_parser.delay(m.khl_id, challenge=m.challenge)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def async_hockey_match_parser(match_id, update=False, challenge=None):
    b'''
        Парсер матча.
    '''
    try:
        parser = challenge.match_parser
        abs_url = challenge.match_url(match_id)
        if update:
            m = models.Match.objects.filter(khl_id=match_id).last()
            if m:
                parser(absolute_url=abs_url).update_model_object(m)
        else:
            parser(absolute_url=abs_url).put_data_in_db_from_page(match_id)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def rhockey_player_parser(player_id):
    try:
        player_id = int(player_id)
        parsers.player.RhockeyPlayerInfoParser().update_player(player_id)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def rhockey_players_parser():
    for i in range(1,99748):
        try:
            rhockey_player_parser.delay(i)
        except Exception, exc:
            logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def probrosanet_player_parser(player):
    try:
        d = parsers.player.ProbrosanetPlayerInfoParser().get_page(player.khl_id)
        if d.get('pos'):
            player.pos = d['pos']
            player.save(update_fields=['pos'])
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def probrosanet_players_parser():
    plrs = models.Player.objects.filter(line=3, khl_id__isnull=False)
    for obj in plrs:
        try:
            probrosanet_player_parser.delay(obj)
        except Exception, exc:
            logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def async_hockey_player_update(id, parser_id):
    b'''
        Обновление инфо о игроке
    '''
    try:
        parser_id = int(parser_id)
        parser = {  1: parsers.player.MHLPlayerInfo,
                    2: parsers.player.KHLPlayerInfo,
                    3: parsers.player.VHLPlayerInfo,
                    4: parsers.player.MHL2PlayerInfo,
        }.get(parser_id)
        if parser:
            data = parser().get_page(id)
            models.Player.objects.get_or_create_player( khl_id=id,
                                                        update=True,
                                                        data=data
            )
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def async_db_players_update():
    b'''
        Обновление инфо о игроке
    '''
    try:
        for player in models.Player.objects.all():
            player.weight = str2int_safe(player.weight_str)
            player.height = str2int_safe(player.height_str)
            player.save(update_fields=['height', 'weight'])
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def async_db_matches_update():
    b'''
        Обновление инфо о матчах
    '''
    try:
        for match_id in models.Match.objects.filter(home_score__isnull=True
                                            ).values_list('id', flat=True):
            async_db_match_update.delay(match_id)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def async_db_match_update(match_id):
    b'''
        Обновление инфо о матче
    '''
    try:
        match = models.Match.objects.get(id=match_id)
        match.count=match.count.strip(
                            ).replace(' ',''
                            ).replace('-:+',''
                            ).replace('(',''
                            ).replace(')','')
        match.home_score = str2int_safe(match.count.split(':')[0])
        match.guest_score = str2int_safe(match.count.split(':'
                                                )[1].replace('Б',''
                                                   ).replace('OT',''
                                                   ).replace('ОТ', ''))
        match.bullet_win = 'Б' in match.count
        match.overtime_win = ('ОТ' in match.count) or ('OT' in match.count)
        match.save(update_fields=['count', 'home_score', 'guest_score',
                                  'overtime_win', 'bullet_win'])
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


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


COUNTERS_FIELDS = (
    'seasons_total', 'matches_total', 'bullet_matches_total',
    'shots_received_total', 'saves_total', 'loose_goals_total',
    'saves_p_average', 'sf_average', 'zero_goals_matches_total',
    'matches_win_total', 'matches_lose_total', 'gamingtime_total',
) + tuple(itertools.chain(*map(
    lambda x: ('%s_total' % x, '%s_average' % x),
    ('goals', 'assists', 'points', 'plus_minus', 'penalty_time'))))


@app.task(ignore_result=True, track_started=True)
def periodic_player_recalc_counters():
    '''
    Update all fields for each group of players,
    update last_match_date
    '''
    qs = models.Player.objects.all()
    # count = qs.count()
    # limit = 100
    # for i in range(0, count, limit):
    #     pks = qs[i:i + limit].values_list('pk', flat=True)
    #     player_recalc_counters.delay(
    #         pks, COUNTERS_FIELDS, update_last_match_date=True)
    for player in qs:
        player_recalc_counters.delay(
            [player.pk], COUNTERS_FIELDS, update_last_match_date=True)


@app.task(ignore_result=True, track_started=True)
def periodic_player_recalc_counters_index():
    '''
    Update index for each field
    '''
    for field in COUNTERS_FIELDS:
        player_recalc_counters_index.delay(field)


insta_api = InstagramAPI(client_id=settings.INSTAGRAM_ID,
                         client_secret=settings.INSTAGRAM_SECRET)

@app.task(ignore_result=True, track_started=True)
def get_instagram_pictures(insta_loc_id, arena, min_timestamp,
                            max_timestamp=None, max_id=None
):
    data, next = insta_api.location_recent_media(location_id=insta_loc_id,
                                                min_timestamp=min_timestamp,
                                                max_timestamp=max_timestamp,
                                                max_id=max_id)
    if data:
        _fn = arena.image_folder_name or 'Instaphotos'
        for item in data:
            if item.type == 'image':
                iif = InstagramImageFile.objects.get_or_create_iif(item, _fn)
                if iif and arena:
                    _crtr = models.ArenaInstaPhoto.objects.get_or_create
                    _crtr(arena=arena,photo=iif)
    if next:
        max_id = re.search('max_id=(\d+)', next).group(0).split('=')[1]
        get_instagram_pictures.delay(  insta_loc_id, arena,
                                        min_timestamp=min_timestamp,
                                        max_timestamp=max_timestamp,
                                        max_id=max_id)


@app.task(ignore_result=True, track_started=True)
def get_arenas_instagram_pictures(min_timestamp=None, max_timestamp=None):
    if min_timestamp:
        min_t = min_timestamp
    else:
        _ts_min = datetime.datetime.today()-datetime.timedelta(days=1)
        min_t = int(time.mktime(_ts_min.timetuple()))
    if max_timestamp:
        max_t = max_timestamp
    else:
        max_t = int(time.mktime(datetime.datetime.today().timetuple()))
    arenas = models.Arena.objects.exclude(coords='')
    for arena in arenas:
        locations = utils.get_arena_instagram_locations(arena.coords)
        for loc_id in locations:
                get_instagram_pictures.delay(loc_id, arena, min_t, max_t)


@app.task(ignore_result=True, track_started=True)
def periodic_player_generate_timeline():
    pks = models.Player.objects.values_list('pk', flat=True)
    for i in range(0, len(pks), 1000):  # 1000 players per task
        timeline_tasks.PlayerTimelineGenerator().delay(pks[i:i + 1000])
