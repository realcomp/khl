# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0087_auto_20150525_1219'),
        ('base', '0017_remove_instagramimagefile_user_str'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerSeasonStat',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('tournament_type', models.CharField(
                    default=b'regular', max_length=16,
                    choices=[
                        (b'regular', 'Regular season'),
                        (b'playoff', 'Playoff'),
                        (b'other', 'Other'),
                    ])),
                ('is_goalie', models.BooleanField(default=False)),
                ('number', models.CharField(max_length=8, blank=True)),
                ('matches', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('goals', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('assists', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('penalty_time', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('points', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('plus_minus', models.SmallIntegerField(null=True, blank=True)),
                ('plus', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('minus', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('es_goals', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('pp_goals', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('sh_goals', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('overtime_goals', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('win_goals', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('bullet_goals', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('shots', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('pis', models.FloatField(null=True, blank=True)),
                ('shots_per_game', models.FloatField(null=True, blank=True)),
                ('faceoff', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('winfaceoff', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('winfaceoff_p', models.FloatField(null=True, blank=True)),
                ('icetime_per_game', models.CharField(max_length=8, blank=True)),
                ('hits', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('blocks', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('fouls', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('takeaways', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('interceptions', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('wins', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('losses', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('bullet_matches', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('shots_received', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('loose_goals', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('saves', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('saves_p', models.FloatField(null=True, blank=True)),
                ('sf', models.FloatField(null=True, blank=True)),
                ('zero_goals_matches', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('gamingtime', models.CharField(max_length=16, blank=True)),
                ('player', models.ForeignKey(
                    related_name='season_stats',
                    to='hockeyapp.Player')),
                ('club', models.ForeignKey(
                    on_delete=django.db.models.deletion.SET_NULL,
                    blank=True, to='hockeyapp.Club', null=True)),
                ('season', models.ForeignKey(
                    on_delete=django.db.models.deletion.SET_NULL,
                    blank=True, to='base.Season', null=True)),
            ],
            options={
                'verbose_name': 'Player Season Stat',
                'verbose_name_plural': 'Player Season Stats',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='playerseasonstat',
            unique_together=set([('player', 'club', 'season', 'tournament_type')]),
        ),
    ]
