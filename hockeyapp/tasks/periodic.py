# -*- coding: utf-8 -*-
import itertools

from sportomatics.celery import app

from . import counters, relatedplayer, timeline_tasks
from .. import models
from .. import timeline_tasks


COUNTERS_FIELDS = (
    'seasons_total', 'matches_total', 'bullet_matches_total',
    'shots_received_total', 'saves_total', 'loose_goals_total',
    'saves_p_average', 'sf_average', 'zero_goals_matches_total',
    'matches_win_total', 'matches_lose_total', 'gamingtime_total',
) + tuple(itertools.chain(*map(
    lambda x: ('%s_total' % x, '%s_average' % x),
    ('goals', 'assists', 'points', 'plus_minus', 'penalty_time'))))


@app.task(ignore_result=True, track_started=True)
def player_recalc_counters():
    '''
    Update all fields for each group of players,
    update last_match_date
    '''
    qs = models.Player.objects.all()
    count = qs.count()
    limit = 100
    for i in range(0, count, limit):
        pks = qs[i:i + limit].values_list('pk', flat=True)
        counters.player_recalc_counters.delay(
            pks, COUNTERS_FIELDS, update_last_match_date=True)


@app.task(ignore_result=True, track_started=True)
def player_recalc_counters_index():
    '''
    Update index for each field
    '''
    for field in COUNTERS_FIELDS:
        counters.player_recalc_counters_index.delay(field)



@app.task(ignore_result=True, track_started=True)
def player_generate_timeline():
    pks = models.Player.objects.values_list('pk', flat=True)
    for i in range(0, len(pks), 1000):  # 1000 players per task
        timeline_tasks.PlayerTimelineGenerator().delay(pks[i:i + 1000])


@app.task(ignore_result=True, track_started=True)
def relatedplayer_calc_player():
    for pk in models.Player.objects.values_list('pk', flat=True):
        relatedplayer.relatedplayer_calc_player.delay(pk)
