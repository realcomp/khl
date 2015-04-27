# -*- coding: utf-8 -*-
import sys

from sportomatics.celery import app

from . import logger, models


@app.task(ignore_result=True, track_started=True)
def relatedplayer_calc_player(pk):
    try:
        models.RelatedPlayer.calc(
            Player.objects.filter(pk=pk),
            Player.objects.all())
    except Exception, exc:
        logger.error(exc, exc_info=sys.exc_info())
