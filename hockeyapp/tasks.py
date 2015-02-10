#coding: utf-8
from __future__ import unicode_literals, print_function
import datetime
import sys

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from sportomatics.celery import app

from base.utils import str2int_safe, str2sec_safe, str2float_safe

from . import parsers
from . import models


@app.task(ignore_result=True, track_started=True)
def club_async_update(links, parser):
    for link in links:
        try:
            parser().put_data_in_db_from_page(link[:-1]) #remove last slash
        except Exception, exc:
            logger.error(exc, exc_info=sys.exc_info())

@app.task(ignore_result=True, track_started=True)
def periodic_update_clubs():
        for links, club_parser in ( 
            (parsers.club.KHLClubURLs().get_page(), parsers.club.KHLClubInfo), 
            (parsers.club.VHLClubURLs().get_page(), parsers.club.VHLClubInfo),
            (parsers.club.MHLClubURLs().get_page(), parsers.club.MHLClubInfo),
            (parsers.club.MHL2ClubURLs().get_page(), parsers.club.MHL2ClubInfo),
        ):
            if club_parser:
                club_async_update.delay(links, club_parser)


@app.task(ignore_result=True, track_started=True)
def periodic_update_schedules():
    _parsers = ((parsers.schedule.KHLScheduleParser, 266),
                (parsers.schedule.VHLScheduleParser, 269),
                (parsers.schedule.MHLScheduleParser, 272),
                (parsers.schedule.MHL2ScheduleParser, 274),
    )
    for _parser, id in _parsers:
        _parser().put_data_in_db_from_page(id,update=True, challenge_type=1)


@app.task(ignore_result=True, track_started=True)
def periodic_get_matches():
    matches = models.Schedule.objects.filter(khl_id__isnull=False,
                                            processed=False,
                                            match__isnull=True)
    for m in matches:
        parser_id = {
                        'MHL': 1,
                        'KHL': 2,
                        'VHL': 3,
                        'MHL-2': 4,
        }.get(m.league.en_title)
        if parser_id:
            async_hockey_match_parser.delay(parser_id, m.khl_id)


@app.task(ignore_result=True, track_started=True)
def async_hockey_match_parser(parser_id, matchid, update=False):
    b'''
        Парсер матча.
    '''
    try:
        parser_id = int(parser_id)
        parser = {  1: parsers.match.HockeyMHLMatchParser,
                    2: parsers.match.HockeyKHLMatchParser,
                    3: parsers.match.HockeyVHLMatchParser,
                    4: parsers.match.HockeyMHL2MatchParser,
        }.get(parser_id, parsers.match.HockeyMHLMatchParser)
        if update:
            m = models.Match.objects.filter(khl_id=matchid).last()
            if m:
                parser().update_model_object(m)
        else:
            parser().put_data_in_db_from_page(matchid)
        #parsers.match.HockeyMHLMatchParser(html=False).get_page(matchid)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def async_hockey_matches_parser(parser_id, match_id, matches, update=False):
    b'''
        Парсер матчей.
        Требует три аргумента:
            1. id парсера
            2. стартовый match_id матча
            3. Счетчик количества match_id
    '''
    for i in range(matches):
        matchid = match_id+i
        try:
            async_hockey_match_parser.delay(parser_id, matchid, update)
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
def mhl_matches_update():
    b'''
        Обновление инфо о матчах в дб
    '''
    try:
        matches = models.Match.objects.filter(html_body__isnull=False
                                     ).filter(url__startswith='http://mhl.khl.ru/report/272/?idgame=')
        for m in matches:
            parser = parsers.match.HockeyMHLMatchParser
            parser().update_model_object(m)
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


@app.task(ignore_result=True, track_started=True)
def async_all_cmps_update():
    try:
        cpms = models.ClubPlayerMatch.objects.filter(shots__isnull=True
                                            ).values_list('id', flat=True)
        for id in cpms:
            async_temp_stats_plr_update.delay(id)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def add_season_for_all():
    try:
        def update_obj(obj):
            if obj.start_date and obj.end_date:
                data = dict(
                    start_date=datetime.date(day=1,month=7,year=obj.start_date.year), 
                    end_date=datetime.date(day=30,month=6,year=obj.end_date.year)
                )
                season, _crt = models.Season.objects.get_or_create_season(**data)
                obj.season = season
                obj.save(update_fields=('season',))

        for obj in models.AddressClub.objects.all():
            update_obj(obj)
        for obj in models.LeagueClub.objects.all():
            update_obj(obj)
        for obj in models.ClubPlayer.objects.all():
            update_obj(obj)
        for obj in models.CoachClub.objects.all():
            update_obj(obj)
        for obj in models.LogoClubHistory.objects.all():
            update_obj(obj)
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def player_recalc_counters(ids):
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
    '''
    try:
        for player in models.Player.objects.filter(id__in=ids):
            player.recalc_counters()
            player.save()
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())


@app.task(ignore_result=True, track_started=True)
def temp_update_schedules():
    '''
        1 - championship,
        2 - playoff,
        3 - hopeful cup
        4 - MHL World Cup
        5 - MHL Challenge Cup
        6 - MHL playout
        7 - MHL qualifying tournament
    '''
    _parsers = (# KHL ######################################
                (parsers.schedule.KHLScheduleParser, 245, 2),
                (parsers.schedule.KHLScheduleParser, 265, 3),
                (parsers.schedule.KHLScheduleParser, 244, 1),
                (parsers.schedule.KHLScheduleParser, 223, 2),
                (parsers.schedule.KHLScheduleParser, 237, 3),
                (parsers.schedule.KHLScheduleParser, 222, 1),
                (parsers.schedule.KHLScheduleParser, 203, 2),
                (parsers.schedule.KHLScheduleParser, 202, 1),
                (parsers.schedule.KHLScheduleParser, 186, 2),
                (parsers.schedule.KHLScheduleParser, 185, 1),
                (parsers.schedule.KHLScheduleParser, 168, 2),
                (parsers.schedule.KHLScheduleParser, 167, 1),
                (parsers.schedule.KHLScheduleParser, 165, 2),
                (parsers.schedule.KHLScheduleParser, 160, 1),
                # MHL #######################################
                (parsers.schedule.MHLScheduleParser, 277, 4),
                (parsers.schedule.MHLScheduleParser, 253, 2),
                (parsers.schedule.MHLScheduleParser, 252, 1),
                (parsers.schedule.MHLScheduleParser, 247, 4),
                (parsers.schedule.MHLScheduleParser, 236, 5),
                (parsers.schedule.MHLScheduleParser, 230, 2),
                (parsers.schedule.MHLScheduleParser, 229, 1),
                (parsers.schedule.MHLScheduleParser, 220, 4),
                (parsers.schedule.MHLScheduleParser, 205, 2),
                (parsers.schedule.MHLScheduleParser, 207, 6),
                (parsers.schedule.MHLScheduleParser, 204, 1),
                (parsers.schedule.MHLScheduleParser, 201, 4),
                (parsers.schedule.MHLScheduleParser, 188, 2),
                (parsers.schedule.MHLScheduleParser, 187, 1),
                (parsers.schedule.MHLScheduleParser, 187, 1),
                (parsers.schedule.MHLScheduleParser, 173, 2),
                (parsers.schedule.MHLScheduleParser, 170, 1),
                (parsers.schedule.MHLScheduleParser, 196, 7),
                # MHL-2 #####################################
                (parsers.schedule.MHL2ScheduleParser, 306, 8),
                (parsers.schedule.MHL2ScheduleParser, 261, 8),
                (parsers.schedule.MHL2ScheduleParser, 238, 8),
                (parsers.schedule.MHL2ScheduleParser, 255, 2),
                (parsers.schedule.MHL2ScheduleParser, 254, 1),
                (parsers.schedule.MHL2ScheduleParser, 234, 2),
                (parsers.schedule.MHL2ScheduleParser, 231, 1),
                (parsers.schedule.MHL2ScheduleParser, 214, 2),
                (parsers.schedule.MHL2ScheduleParser, 211, 1),
                # VHL ########################################
                (parsers.schedule.VHLScheduleParser, 251, 2),
                (parsers.schedule.VHLScheduleParser, 250, 1),
                (parsers.schedule.VHLScheduleParser, 228, 2),
                (parsers.schedule.VHLScheduleParser, 227, 1),
                (parsers.schedule.VHLScheduleParser, 209, 2),
                (parsers.schedule.VHLScheduleParser, 208, 1),
                (parsers.schedule.VHLScheduleParser, 190, 2),
                (parsers.schedule.VHLScheduleParser, 189, 1),
    )
    for _parser, id, chlng_type in _parsers:
        _parser().put_data_in_db_from_page( id, update=True,
                                            challenge_type=chlng_type,
                                            without_khl_id=False,
        )