# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0018_auto_20150112_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubplayermatch',
            name='bullet_goals',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Win Bullet Goals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='es_goals',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Even Strength Goals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='ev_goals',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='EV Goals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='faceoff',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Face-off'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='gamingtime',
            field=models.PositiveIntegerField(null=True, verbose_name='Gaming time'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='loose_goals',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Loose Goals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='overtime_goals',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Overtime Goals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='penalty_time',
            field=models.PositiveIntegerField(null=True, verbose_name='Penalty Time, sec'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='pis',
            field=models.FloatField(null=True, verbose_name='Percentage of Implemented Shots'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='plus_minus',
            field=models.SmallIntegerField(null=True, verbose_name='+/-'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='pp_goals',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Power Play Goals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='saves',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Saves Goals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='saves_p',
            field=models.FloatField(null=True, verbose_name='Saves Goals Percentage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='sf',
            field=models.FloatField(null=True, verbose_name='Safety Factor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='shots',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Shots count'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='win_goals',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Win Goals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='winfaceoff',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Face-off Wins'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='winfaceoff_p',
            field=models.FloatField(null=True, verbose_name='Face-off Wins Percentage'),
            preserve_default=True,
        ),
    ]
