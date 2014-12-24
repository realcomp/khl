# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0004_auto_20141223_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancedPlayerStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shots_1th', models.CharField(max_length=16, verbose_name='1th period Shots', blank=True)),
                ('shots_2nd', models.CharField(max_length=16, verbose_name='2nd period Shots', blank=True)),
                ('shots_3th', models.CharField(max_length=16, verbose_name='3th period Shots', blank=True)),
                ('shots_all', models.CharField(max_length=16, verbose_name='All periods Shots', blank=True)),
                ('faceoff_1th', models.CharField(max_length=16, verbose_name='1th period Faceoffs', blank=True)),
                ('faceoff_2nd', models.CharField(max_length=16, verbose_name='2nd period Faceoffs', blank=True)),
                ('faceoff_3th', models.CharField(max_length=16, verbose_name='3th period Faceoffs', blank=True)),
                ('faceoff_all', models.CharField(max_length=16, verbose_name='All periods Faceoffs', blank=True)),
                ('change_count_1th', models.CharField(max_length=16, verbose_name='1th period change count', blank=True)),
                ('gamingtime_1th', models.CharField(max_length=16, verbose_name='1th period time in game', blank=True)),
                ('change_count_2nd', models.CharField(max_length=16, verbose_name='2nd period change count', blank=True)),
                ('gamingtime_2nd', models.CharField(max_length=16, verbose_name='2nd period change count', blank=True)),
                ('change_count_3th', models.CharField(max_length=16, verbose_name='3th period change count', blank=True)),
                ('gamingtime_3th', models.CharField(max_length=16, verbose_name='3th period time in game', blank=True)),
                ('change_count_all', models.CharField(max_length=16, verbose_name='All periods change count', blank=True)),
                ('gamingtime_all', models.CharField(max_length=16, verbose_name='All periods time in game', blank=True)),
                ('block_1th', models.CharField(max_length=16, verbose_name='1th period blocks', blank=True)),
                ('hit_1th', models.CharField(max_length=16, verbose_name='1th period hits', blank=True)),
                ('foul_1th', models.CharField(max_length=16, verbose_name='1th period fouls', blank=True)),
                ('block_2nd', models.CharField(max_length=16, verbose_name='2nd period blocks', blank=True)),
                ('hit_2nd', models.CharField(max_length=16, verbose_name='2nd period hits', blank=True)),
                ('foul_2nd', models.CharField(max_length=16, verbose_name='2nd period fouls', blank=True)),
                ('block_3th', models.CharField(max_length=16, verbose_name='3th period blocks', blank=True)),
                ('hit_3th', models.CharField(max_length=16, verbose_name='3th period hits', blank=True)),
                ('foul_3th', models.CharField(max_length=16, verbose_name='3th period fouls', blank=True)),
                ('block_all', models.CharField(max_length=16, verbose_name='All periods blocks', blank=True)),
                ('hit_all', models.CharField(max_length=16, verbose_name='All periods hits', blank=True)),
                ('foul_all', models.CharField(max_length=16, verbose_name='All periods fouls', blank=True)),
            ],
            options={
                'verbose_name': 'Player Stats',
                'verbose_name_plural': 'Players Stats',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='adv_stats',
            field=models.OneToOneField(null=True, blank=True, to='hockeyapp.AdvancedPlayerStats'),
            preserve_default=True,
        ),
    ]
