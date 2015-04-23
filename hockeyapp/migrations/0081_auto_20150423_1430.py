# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0080_relatedplayer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relatedplayer',
            name='value',
        ),
        migrations.AddField(
            model_name='relatedplayer',
            name='assists_value',
            field=models.FloatField(null=True, verbose_name='Similarity by Assists', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relatedplayer',
            name='goals_value',
            field=models.FloatField(null=True, verbose_name='Similarity by Goals', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relatedplayer',
            name='penalty_time_value',
            field=models.FloatField(null=True, verbose_name='Similarity by Penalty time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relatedplayer',
            name='plus_minus_value',
            field=models.FloatField(null=True, verbose_name='Similarity by +/-', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relatedplayer',
            name='points_value',
            field=models.FloatField(null=True, verbose_name='Similarity by Points', blank=True),
            preserve_default=True,
        ),
    ]
