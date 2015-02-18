# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0052_auto_20150216_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubphotos',
            name='proccesed_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 17, 11, 15, 40, 650583, tzinfo=utc), verbose_name='Processed time', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clubphotos',
            name='processed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
