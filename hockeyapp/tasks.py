#coding: utf-8
from __future__ import unicode_literals, print_function
import datetime
import itertools
import operator
import re
import sys
import time

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from django.conf import settings
from django.db.models import Q

from sportomatics.celery import app

from instagram.client import InstagramAPI

from base.models import InstagramImageFile
from base.utils import str2int_safe, str2sec_safe, str2float_safe

from . import parsers
from . import models
from . import utils


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


#@app.task(ignore_result=True, track_started=True)
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


#@app.task(ignore_result=True, track_started=True)
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


#@app.task(ignore_result=True, track_started=True)
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


#@app.task(ignore_result=True, track_started=True)
#def temp_update_schedules():
    #'''
        #1 - championship,
        #2 - playoff,
        #3 - hopeful cup
        #4 - MHL World Cup
        #5 - MHL Challenge Cup
        #6 - MHL playout
        #7 - MHL qualifying tournament
    #'''
    #_parsers = (# KHL ######################################
                #(parsers.schedule.KHLScheduleParser, 245, 2),
                #(parsers.schedule.KHLScheduleParser, 265, 3),
                #(parsers.schedule.KHLScheduleParser, 244, 1),
                #(parsers.schedule.KHLScheduleParser, 223, 2),
                #(parsers.schedule.KHLScheduleParser, 237, 3),
                #(parsers.schedule.KHLScheduleParser, 222, 1),
                #(parsers.schedule.KHLScheduleParser, 203, 2),
                #(parsers.schedule.KHLScheduleParser, 202, 1),
                #(parsers.schedule.KHLScheduleParser, 186, 2),
                #(parsers.schedule.KHLScheduleParser, 185, 1),
                #(parsers.schedule.KHLScheduleParser, 168, 2),
                #(parsers.schedule.KHLScheduleParser, 167, 1),
                #(parsers.schedule.KHLScheduleParser, 165, 2),
                #(parsers.schedule.KHLScheduleParser, 160, 1),
                ## MHL #######################################
                #(parsers.schedule.MHLScheduleParser, 277, 4),
                #(parsers.schedule.MHLScheduleParser, 253, 2),
                #(parsers.schedule.MHLScheduleParser, 252, 1),
                #(parsers.schedule.MHLScheduleParser, 247, 4),
                #(parsers.schedule.MHLScheduleParser, 236, 5),
                #(parsers.schedule.MHLScheduleParser, 230, 2),
                #(parsers.schedule.MHLScheduleParser, 229, 1),
                #(parsers.schedule.MHLScheduleParser, 220, 4),
                #(parsers.schedule.MHLScheduleParser, 205, 2),
                #(parsers.schedule.MHLScheduleParser, 207, 6),
                #(parsers.schedule.MHLScheduleParser, 204, 1),
                #(parsers.schedule.MHLScheduleParser, 201, 4),
                #(parsers.schedule.MHLScheduleParser, 188, 2),
                #(parsers.schedule.MHLScheduleParser, 187, 1),
                #(parsers.schedule.MHLScheduleParser, 187, 1),
                #(parsers.schedule.MHLScheduleParser, 173, 2),
                #(parsers.schedule.MHLScheduleParser, 170, 1),
                #(parsers.schedule.MHLScheduleParser, 196, 7),
                ## MHL-2 #####################################
                #(parsers.schedule.MHL2ScheduleParser, 306, 8),
                #(parsers.schedule.MHL2ScheduleParser, 261, 8),
                #(parsers.schedule.MHL2ScheduleParser, 238, 8),
                #(parsers.schedule.MHL2ScheduleParser, 255, 2),
                #(parsers.schedule.MHL2ScheduleParser, 254, 1),
                #(parsers.schedule.MHL2ScheduleParser, 234, 2),
                #(parsers.schedule.MHL2ScheduleParser, 231, 1),
                #(parsers.schedule.MHL2ScheduleParser, 214, 2),
                #(parsers.schedule.MHL2ScheduleParser, 211, 1),
                ## VHL ########################################
                #(parsers.schedule.VHLScheduleParser, 251, 2),
                #(parsers.schedule.VHLScheduleParser, 250, 1),
                #(parsers.schedule.VHLScheduleParser, 228, 2),
                #(parsers.schedule.VHLScheduleParser, 227, 1),
                #(parsers.schedule.VHLScheduleParser, 209, 2),
                #(parsers.schedule.VHLScheduleParser, 208, 1),
                #(parsers.schedule.VHLScheduleParser, 190, 2),
                #(parsers.schedule.VHLScheduleParser, 189, 1),
    #)
    #for _parser, id, chlng_type in _parsers:
        #_parser().put_data_in_db_from_page( id, update=False,
                                            #challenge_type=chlng_type,
                                            #without_khl_id=False,
        #)


@app.task(ignore_result=True, track_started=True)
def player_generate_timeline(ids):
    def birthday_events(players):
        # birthday events
        timelines = models.Timeline.objects.filter(type='birthday')
        for player in players.exclude(
                pk__in=timelines.values_list('player_id', flat=True)):
            models.Timeline.objects.create(
                start_date=player.birth_date,
                ru_headline='День рождения',
                en_headline='Birth day',
                ru_text='День рождения',
                en_text='Birth day',
                media=player.photo,
                type='birthday',
                player=player)

    def first_event(players, **kwargs):
        ''' abstract 1st event factory '''
        timelines = models.Timeline.objects.filter(type=kwargs['type'])
        for player in players.exclude(
                pk__in=timelines.values_list('player_id', flat=True)):
            try:
                date = kwargs['date_query'](player)
            except kwargs['date_model'].DoesNotExist:
                pass
            else:
                models.Timeline.objects.create(
                    start_date=date,
                    ru_headline=kwargs['ru_headline'],
                    en_headline=kwargs['en_headline'],
                    ru_text=kwargs['ru_text'],
                    en_text=kwargs['en_text'],
                    media=player.photo,
                    type=kwargs['type'],
                    player=player)

    def first_goal_event(players):
        def date_query(player):
            return (
                models.MatchGoalHistory.objects
                .filter(scorer=player)
                .earliest('match__date').match.date)
        first_event(
            players,
            type='first_goal',
            date_query=date_query,
            date_model=models.MatchGoalHistory,
            ru_headline='Первая шайба в карьере',
            en_headline='First goal in career',
            ru_text='Первая шайба в карьере',
            en_text='First goal in career')

    def first_hat_trick_event(players):
        def date_query(player):
            return (
                models.ClubPlayerMatch.objects
                .filter(clubplayer__player=player, goals=3)
                .earliest('match__date').match.date)
        first_event(
            players,
            type='first_hat_trick',
            date_query=date_query,
            date_model=models.ClubPlayerMatch,
            ru_headline='Первый "хет-трик" в карьере',
            en_headline='First hat trick in career',
            ru_text='Первый "хет-трик" в карьере',
            en_text='First hat trick in career')

    def first_poker_event(players):
        def date_query(player):
            return (
                models.ClubPlayerMatch.objects
                .filter(clubplayer__player=player, goals=4)
                .earliest('match__date').match.date)
        first_event(
            players,
            type='first_poker',
            date_query=date_query,
            date_model=models.ClubPlayerMatch,
            ru_headline='Первый "покер" в карьере',
            en_headline='First poker in career',
            ru_text='Первый "покер" в карьере',
            en_text='First poker in career')

    def first_0_loose_goals_event(players):
        def date_query(player):
            # line=1 goalkeeper
            return (
                models.ClubPlayerMatch.objects
                .filter(
                    clubplayer__player=player, clubplayer__line=1,
                    loose_goals=0)
                .earliest('match__date').match.date)
        first_event(
            players,
            type='first_0_loose_goals',
            date_query=date_query,
            date_model=models.ClubPlayerMatch,
            ru_headline='Первый "сухарь" в карьере',
            en_headline='First 0 loose goals in career',
            ru_text='Первый "сухарь" в карьере',
            en_text='First 0 loose goals in career')

    def first_loose_goal_event(players):
        def date_query(player):
            # line=1 goalkeeper
            return (
                models.ClubPlayerMatch.objects
                .filter(
                    clubplayer__player=player, clubplayer__line=1,
                    loose_goals__gte=1)
                .earliest('match__date').match.date)
        first_event(
            players,
            type='first_loose_goal',
            date_query=date_query,
            date_model=models.ClubPlayerMatch,
            ru_headline='Первый гол в карьере',
            en_headline='First loose goal in career',
            ru_text='Первый гол в карьере',
            en_text='First loose goal in career')

    def first_match_event(players):
        def date_query(player):
            return (
                models.ClubPlayerMatch.objects
                .filter(clubplayer__player=player)
                .earliest('match__date').match.date)
        first_event(
            players,
            type='first_match',
            date_query=date_query,
            date_model=models.ClubPlayerMatch,
            ru_headline='Первый матч в карьере',
            en_headline='First match in career',
            ru_text='Первый матч в карьере',
            en_text='First match in career')

    def goals_events(players):
        for player in players:
            count = (
                models.Timeline.objects
                .filter(type='goals', player=player).count())
            goals = (
                models.MatchGoalHistory.objects
                .filter(scorer=player)
                .order_by('match__date'))
            if goals.count() > 0 and goals.count() / 50 > count:
                for i, goal in enumerate(goals):
                    if i + 1 > count * 50 and not (i + 1) % 50:
                        models.Timeline.objects.create(
                            start_date=goal.match.date,
                            ru_headline='%d-я шайба в карьере' % (i + 1),
                            en_headline='%dth goal in career' % (i + 1),
                            ru_text='%d-я шайба в карьере' % (i + 1),
                            en_text='%dth goal in career' % (i + 1),
                            media=player.photo,
                            type='goals',
                            player=player)

    def points_events(players):
        for player in players:
            count = (
                models.Timeline.objects
                .filter(type='goals', player=player).count())
            matches = (
                models.ClubPlayerMatch.objects
                .filter(clubplayer__player=player)
                .exclude(points=0)
                .order_by('match__date'))
            i = 0
            target = 50
            for match in matches:
                i += match.points or 0
                if i >= target:
                    target += 50
                    if not models.Timeline.objects.filter(
                            start_date=match.match.date,
                            type='points',
                            player=player).exists():
                        models.Timeline.objects.create(
                            start_date=match.match.date,
                            ru_headline='%d-е очко в карьере' % i,
                            en_headline='%dth point in career' % i,
                            ru_text='%d-е очко в карьере' % i,
                            en_text='%dth point in career' % i,
                            media=player.photo,
                            type='points',
                            player=player)

    def matches_events(players):
        for player in players:
            count = (
                models.Timeline.objects
                .filter(type='matches', player=player).count())
            matches = (
                models.ClubPlayerMatch.objects
                .filter(clubplayer__player=player)
                .order_by('match__date'))
            if matches.count() > 0 and matches.count() / 50 > count:
                for i, match in enumerate(matches):
                    if i + 1 > count * 50 and not (i + 1) % 50:
                        models.Timeline.objects.create(
                            start_date=match.match.date,
                            ru_headline='%d-й матч в карьере' % (i + 1),
                            en_headline='%dth match in career' % (i + 1),
                            ru_text='%d-й матч в карьере' % (i + 1),
                            en_text='%dth match in career' % (i + 1),
                            media=player.photo,
                            type='matches',
                            player=player)

    def club_matches_events(players):
        for player in players:
            matches = (
                models.ClubPlayerMatch.objects
                .filter(clubplayer__player=player)
                .order_by('match__date'))
            clubs = (
                models.Club.objects.filter(
                    Q(pk__in=matches.values_list('match__home_team_id')) |
                    Q(pk__in=matches.values_list('match__guest_team_id'))))

            for club in set(clubs):
                count = (
                    models.Timeline.objects
                    .filter(type='club_matches', player=player, club=club)
                    .count())
                matches = (
                    models.ClubPlayerMatch.objects
                    .filter(clubplayer__player=player)
                    .by_club(club, player)
                    .order_by('match__date')
                    .distinct())
                if matches.count() > 0 and matches.count() / 100 > count:
                    for i, match in enumerate(matches):
                        if i + 1 > count * 100 and not (i + 1) % 100:
                            ru_club = club.ru_title
                            en_club = club.en_title
                            models.Timeline.objects.create(
                                start_date=match.match.date,
                                ru_headline='%d-й матч в клубе "%s"' % ((i + 1), ru_club),
                                en_headline='%dth match in a club "%s"' % ((i + 1), en_club),
                                ru_text='%d-й матч в клубе "%s"' % ((i + 1), ru_club),
                                en_text='%dth match in a club "%s"' % ((i + 1), ru_club),
                                media=club.logo,
                                type='club_matches',
                                player=player,
                                club=club)

    def club_change_events(players):
        for player in players:
            dates = (
                models.Timeline.objects
                .filter(type='club_change', player=player)
                .values_list('start_date', flat=True))
            clubplayers = (
                models.ClubPlayer.objects
                .filter(player=player)
                .exclude(start_date__in=dates)
                .order_by('start_date'))

            # group by club
            timelines = {}
            for clubplayer in clubplayers:
                ru_club = clubplayer.club.ru_title
                en_club = clubplayer.club.en_title
                url = clubplayer.club_url
                timeline = models.Timeline(
                    start_date=clubplayer.start_date,
                    end_date=clubplayer.end_date,
                    ru_headline='В составе клуба "%s"' % ru_club,
                    en_headline='Membership in a club "%s"' % en_club,
                    ru_text='В составе клуба "%s"' % ru_club,
                    en_text='Membership in a club "%s"' % en_club,
                    media=clubplayer.club.logo,
                    media_caption='<a href="%s">-&gt;</a>' % url,
                    type='club_change',
                    player=player,
                    club=clubplayer.club)

                if clubplayer.club.pk not in timelines:
                    timelines[clubplayer.club.pk] = [timeline]
                else:
                    date_a = timelines[clubplayer.club.pk][-1].end_date
                    date_b = clubplayer.start_date
                    # extra day between the same events is ignored
                    if date_a + datetime.timedelta(days=1) >= date_b:
                        # combine events by shifting end date
                        timelines[clubplayer.club.pk][-1].end_date = clubplayer.end_date
                    else:
                        timelines[clubplayer.club.pk].append(timeline)
            models.Timeline.objects.bulk_create(
                itertools.chain(*timelines.values()))

    def first_club_goal_event(players):
        club_changes = (
            models.Timeline.objects
            .filter(type='club_change', player__in=players))

        for player in players:
            player_club_changes = club_changes.filter(player=player)

            timelines = (
                models.Timeline.objects
                .filter(type='first_club_goal', player=player))
            if timelines.exists():
                # ~Q & ~Q & ~Q
                q_existing = reduce(operator.and_, map(
                    lambda x: ~Q(start_date=x.start_date, club=x.club),
                    timelines))
                player_club_changes = player_club_changes.filter(q_existing)

            for club_change in player_club_changes:
                try:
                    history = (
                        models.MatchGoalHistory.objects
                        .filter(
                            scorer=club_change.player,
                            match__date__gte=club_change.start_date,
                            match__date__lte=club_change.end_date)
                        .by_club(club_change.club, club_change.player)
                        .earliest('match__date'))
                except models.MatchGoalHistory.DoesNotExist:
                    pass
                else:
                    ru_club = club_change.club.ru_title
                    en_club = club_change.club.en_title
                    models.Timeline.objects.get_or_create(
                        start_date=history.match.date,
                        ru_headline='Первая шайба в клубе "%s"' % ru_club,
                        en_headline='First goal in a club "%s"' % en_club,
                        ru_text='Первая шайба в клубе "%s"' % ru_club,
                        en_text='First goal in a club "%s"' % en_club,
                        media=club_change.club.logo,
                        type='first_club_goal',
                        player=club_change.player,
                        club=club_change.club)

    def series_0_loose_goals_event(players):
        for player in players:
            matches = (
                models.ClubPlayerMatch.objects
                .filter(
                    clubplayer__player=player, clubplayer__line=1)
                .order_by('match__date'))
            i = 0
            for match in matches:
                if match.loose_goals == 0:
                    i += 1
                else:
                    i = 0
                if i >= 3 and not models.Timeline.objects.filter(
                        start_date=match.match.date,
                        type='series_0_loose_goals',
                        player=player).exists():
                    models.Timeline.objects.create(
                        start_date=match.match.date,
                        ru_headline='%d-й "сухарь" подряд' % i,
                        en_headline='%dth in series of 0 loose goals' % i,
                        ru_text='%d-й "сухарь" подряд' % i,
                        en_text='%dth in series of 0 loose goals' % i,
                        media=player.photo,
                        type='series_0_loose_goals',
                        player=player)

    players = models.Player.objects.filter(pk__in=ids)

    birthday_events(players)
    first_goal_event(players)
    first_hat_trick_event(players)
    first_poker_event(players)
    first_0_loose_goals_event(players)
    first_loose_goal_event(players)
    first_match_event(players)
    goals_events(players)
    points_events(players)
    matches_events(players)
    club_matches_events(players)
    club_change_events(players)
    first_club_goal_event(players)
    series_0_loose_goals_event(players)
