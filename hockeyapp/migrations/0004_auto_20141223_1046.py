# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0003_auto_20141222_0937'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clubplayermatch',
            options={'verbose_name': 'Club Player History Match', 'verbose_name_plural': 'Club Player Histories in Matches'},
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='clubplayers',
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='bullet_goals',
            field=models.CharField(max_length=8, null=True, verbose_name='Win Bullet Goals', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='clubplayer',
            field=models.ForeignKey(default=1, to='hockeyapp.ClubPlayer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='es_goals',
            field=models.CharField(max_length=8, null=True, verbose_name='Even Strength Goals', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='ev_goals',
            field=models.CharField(max_length=8, null=True, verbose_name='EV Goals', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='faceoff',
            field=models.CharField(max_length=8, null=True, verbose_name='Face-off', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='gamingtime',
            field=models.CharField(max_length=8, null=True, verbose_name='Gaming time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='loose_goals',
            field=models.CharField(max_length=8, null=True, verbose_name='Loose Goals', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='overtime_goals',
            field=models.CharField(max_length=8, null=True, verbose_name='Overtime Goals', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='penalty_time',
            field=models.CharField(max_length=8, null=True, verbose_name='Penalty Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='pis',
            field=models.CharField(max_length=8, null=True, verbose_name='Percentage of Implemented Shots', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='plus_minus',
            field=models.CharField(max_length=8, null=True, verbose_name='+/-', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='pp_goals',
            field=models.CharField(max_length=8, null=True, verbose_name='Power Play Goals', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='saves',
            field=models.CharField(max_length=8, null=True, verbose_name='Saves Goals', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='saves_p',
            field=models.CharField(max_length=8, null=True, verbose_name='Saves Goals Percentage', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='sf',
            field=models.CharField(max_length=8, null=True, verbose_name='Safety Factor', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='shots',
            field=models.CharField(max_length=8, null=True, verbose_name='Shots count', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='win_goals',
            field=models.CharField(max_length=8, null=True, verbose_name='Win Goals', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='winfaceoff',
            field=models.CharField(max_length=8, null=True, verbose_name='Face-off Wins', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='winfaceoff_p',
            field=models.CharField(max_length=8, null=True, verbose_name='Face-off Wins Percentage', blank=True),
            preserve_default=True,
        ),
    ]
