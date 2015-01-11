# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0014_auto_20150109_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachclub',
            name='head',
            field=models.BooleanField(default=True, verbose_name='Head coach'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='advancedplayerstats',
            name='gamingtime_1th',
            field=models.PositiveIntegerField(null=True, verbose_name='1th period time in game, sec'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='advancedplayerstats',
            name='gamingtime_2nd',
            field=models.PositiveIntegerField(null=True, verbose_name='2nd period time in game, sec'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='advancedplayerstats',
            name='gamingtime_3th',
            field=models.PositiveIntegerField(null=True, verbose_name='3th period time in game, sec'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='advancedplayerstats',
            name='gamingtime_all',
            field=models.PositiveIntegerField(null=True, verbose_name='All periods time in game, sec'),
            preserve_default=True,
        ),
    ]
