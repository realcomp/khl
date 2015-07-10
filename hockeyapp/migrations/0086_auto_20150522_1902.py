# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0085_auto_20150514_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='bullet_goals_total',
            field=models.IntegerField(null=True, verbose_name='Win Bullet Goals Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='es_goals_total',
            field=models.IntegerField(null=True, verbose_name='Even Strength Goals Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='ev_goals_total',
            field=models.IntegerField(null=True, verbose_name='EV Goals Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='overtime_goals_total',
            field=models.IntegerField(null=True, verbose_name='Overtime Goals Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='pp_goals_total',
            field=models.IntegerField(null=True, verbose_name='Power Play Goals Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='win_goals_total',
            field=models.IntegerField(null=True, verbose_name='Win Goals Total'),
            preserve_default=True,
        ),
    ]
