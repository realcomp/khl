# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models
import django.db.models.deletion
import hockeyapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_remove_instagramimagefile_user_str'),
        ('hockeyapp', '0069_player_pos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('title', models.CharField(verbose_name='Title from parser', max_length=1024, editable=False, blank=True)),
                ('khl_id', models.PositiveIntegerField(verbose_name='Other site calendar ID')),
                ('url', models.URLField(verbose_name='Challenge calendar for parsing', blank=True)),
                ('parser_type', models.CharField(blank=True, max_length=255, verbose_name='Parser', choices=[('KHLScheduleParser', 'KHL Schedule Parser'), ('VHLScheduleParser', 'MHL Schedule Parser'), ('MHLScheduleParser', 'MHL Schedule Parser'), ('MHL2ScheduleParser', 'MHL2 Schedule Parser')])),
                ('challenge_type', models.PositiveSmallIntegerField(null=True, verbose_name='Challenge Type', choices=[(0, 'unknown'), (1, 'Championship'), (2, 'Playoff'), (3, 'Hopeful cup'), (4, 'Junior World Cup'), (5, 'Challenge Cup'), (6, 'MHL playout'), (7, 'MHL qualifying tournament'), (8, 'MHL-2 Generation Cup')])),
                ('processed', models.BooleanField(default=False)),
                ('proccesed_time', models.DateTimeField(auto_now=True, verbose_name='Processed time', null=True)),
                ('league', models.ForeignKey(to='hockeyapp.League')),
                ('season', models.ForeignKey(blank=True, to='base.Season', null=True)),
            ],
            options={
                'verbose_name': 'Challenge',
                'verbose_name_plural': 'Challenges',
            },
            bases=(base.models.LocaleAttrMixin, models.Model),
        ),
        migrations.AddField(
            model_name='schedule',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Challenge', to='hockeyapp.Challenge', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schedule',
            name='match_url',
            field=models.URLField(default='', verbose_name='Match Other site url', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='club',
            name='rgb',
            field=models.CharField(validators=[hockeyapp.models.hex_validator], max_length=255, blank=True, help_text='Color hex. Example: #00ffaa', null=True, verbose_name='RGB'),
            preserve_default=True,
        ),
    ]
