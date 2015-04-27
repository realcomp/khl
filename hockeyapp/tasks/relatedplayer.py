# -*- coding: utf-8 -*-
import sys

from sportomatics.celery import app

from . import logger, models


@app.task(ignore_result=True, track_started=True)
def relatedplayer_calc_player(pk):
    try:
        models.RelatedPlayer.calc(
            models.Player.objects.filter(pk=pk))
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())
