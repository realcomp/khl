# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0077_auto_20150408_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubplayermatch',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 10, 16, 19, 44, 739157, tzinfo=utc), verbose_name='Created date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='last_match_date',
            field=models.DateTimeField(null=True, verbose_name='Last match history parsed'),
            preserve_default=True,
        ),
    ]
