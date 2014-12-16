# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
        ('filer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressClub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='Start date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='End date', blank=True)),
                ('address', models.ForeignKey(to='addresses.Address')),
            ],
            options={
                'verbose_name': 'Club address',
                'verbose_name_plural': 'Club addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('opening_dt', models.DateField(null=True, verbose_name='Founding date', blank=True)),
                ('closing_dt', models.DateField(null=True, verbose_name='Closing date', blank=True)),
                ('site', models.URLField(verbose_name='Site', blank=True)),
                ('address', models.ForeignKey(blank=True, to='addresses.Address', null=True)),
            ],
            options={
                'verbose_name': 'Club',
                'verbose_name_plural': 'Clubs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClubPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField(default=0, verbose_name='Number')),
                ('line', models.PositiveSmallIntegerField(default=0, verbose_name='Line', choices=[(0, 'unknown'), (1, 'Goalkeeper'), (2, 'Defender'), (3, 'Offender')])),
                ('start_date', models.DateField(null=True, verbose_name='Start date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='End date', blank=True)),
                ('club', models.ForeignKey(to='hockeyapp.Club')),
            ],
            options={
                'verbose_name': 'Club player',
                'verbose_name_plural': 'Club players',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClubPlayerMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clubplayers', models.ManyToManyField(to='hockeyapp.ClubPlayer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_fio', models.CharField(max_length=4096, verbose_name='Full name (rus)', blank=True)),
                ('en_fio', models.CharField(max_length=4096, verbose_name='Full name (en)', blank=True)),
            ],
            options={
                'verbose_name': 'Coach',
                'verbose_name_plural': 'Coaches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoachClub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='Start date')),
                ('end_date', models.DateField(null=True, verbose_name='End date')),
                ('club', models.ForeignKey(to='hockeyapp.Club')),
                ('coach', models.ForeignKey(to='hockeyapp.Coach')),
            ],
            options={
                'verbose_name': 'Club coach',
                'verbose_name_plural': 'Club coaches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_fio', models.CharField(max_length=4096, verbose_name='Full name (rus)', blank=True)),
                ('en_fio', models.CharField(max_length=4096, verbose_name='Full name (en)', blank=True)),
            ],
            options={
                'verbose_name': 'Judge',
                'verbose_name_plural': 'Judges',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('khl_id', models.PositiveIntegerField(max_length=1024, verbose_name='Other site ID', blank=True)),
                ('proccesed_time', models.DateTimeField(auto_now_add=True, verbose_name='Processed time')),
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('html_body', models.TextField(verbose_name='Parse HTML', blank=True)),
                ('spectators', models.CharField(max_length=1024, verbose_name='Spectators count', blank=True)),
                ('date', models.CharField(max_length=1024, verbose_name='Match date', blank=True)),
                ('count', models.CharField(max_length=1024, verbose_name='Match count', blank=True)),
                ('detail_count', models.CharField(max_length=1024, verbose_name='Match detail count', blank=True)),
                ('guest_coach', models.ForeignKey(related_name='guestmatches', blank=True, to='hockeyapp.Coach', null=True)),
                ('guest_players', models.ManyToManyField(related_name='guestmatches', null=True, to='hockeyapp.ClubPlayer', blank=True)),
                ('guest_team', models.ForeignKey(related_name='guestmatches', verbose_name='Guest team', blank=True, to='hockeyapp.Club', null=True)),
                ('home_coach', models.ForeignKey(related_name='homematches', blank=True, to='hockeyapp.Coach', null=True)),
                ('home_players', models.ManyToManyField(related_name='homematches', null=True, to='hockeyapp.ClubPlayer', blank=True)),
                ('home_team', models.ForeignKey(related_name='homematches', verbose_name='Home team', blank=True, to='hockeyapp.Club', null=True)),
                ('judges', models.ManyToManyField(related_name='matchjudges', null=True, verbose_name='Judges', to='hockeyapp.Judge', blank=True)),
                ('line_judges', models.ManyToManyField(related_name='matchllinejudges', null=True, verbose_name='Line judges', to='hockeyapp.Judge', blank=True)),
            ],
            options={
                'ordering': ('-khl_id',),
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchGoalHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parity', models.PositiveSmallIntegerField(default=0, choices=[(0, 'unknown'), (1, 'EV'), (2, 'POWER PLAYS'), (3, 'EVEN STRENGTH'), (4, 'BULLET')])),
                ('time', models.CharField(max_length=16, blank=True)),
                ('description', models.CharField(max_length=1024, blank=True)),
                ('period', models.CharField(max_length=32, blank=True)),
                ('home_five_numbers', models.CharField(max_length=1024, blank=True)),
                ('guest_five_numbers', models.CharField(max_length=1024, blank=True)),
            ],
            options={
                'verbose_name': 'Match goal entry',
                'verbose_name_plural': 'Match goal entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchPenaltyHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ptype', models.CharField(max_length=1024, blank=True)),
                ('time', models.CharField(max_length=32, blank=True)),
                ('duration', models.CharField(max_length=32, blank=True)),
                ('match', models.ForeignKey(to='hockeyapp.Match')),
            ],
            options={
                'verbose_name': 'Match penalty entry',
                'verbose_name_plural': 'Match penalty entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_fio', models.CharField(max_length=4096, verbose_name='Full name (rus)', blank=True)),
                ('en_fio', models.CharField(max_length=4096, verbose_name='Full name (en)', blank=True)),
                ('khl_id', models.PositiveIntegerField(default=0)),
                ('line', models.PositiveSmallIntegerField(default=0, verbose_name='Line', choices=[(0, 'unknown'), (1, 'Goalkeeper'), (2, 'Defender'), (3, 'Offender')])),
                ('birth_date', models.DateField(null=True, verbose_name='Birth date', blank=True)),
                ('weight', models.CharField(max_length=32, verbose_name='Weight', blank=True)),
                ('height', models.CharField(max_length=32, verbose_name='Height', blank=True)),
                ('photo', filer.fields.image.FilerImageField(verbose_name='Photo', blank=True, to='filer.Image', null=True)),
            ],
            options={
                'verbose_name': 'Player',
                'verbose_name_plural': 'Players',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='matchpenaltyhistory',
            name='player',
            field=models.ForeignKey(related_name='penaltymatch', to='hockeyapp.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matchgoalhistory',
            name='assist',
            field=models.ManyToManyField(related_name='goalassistmatch', null=True, to='hockeyapp.Player', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matchgoalhistory',
            name='match',
            field=models.ForeignKey(to='hockeyapp.Match'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matchgoalhistory',
            name='scorer',
            field=models.ForeignKey(related_name='goalscorermatch', to='hockeyapp.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='match',
            field=models.ForeignKey(to='hockeyapp.Match'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayer',
            name='player',
            field=models.ForeignKey(to='hockeyapp.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='coach',
            field=models.ForeignKey(blank=True, to='hockeyapp.Coach', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='logo',
            field=filer.fields.image.FilerImageField(verbose_name='Logo', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='players',
            field=models.ManyToManyField(to='hockeyapp.Player', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='addressclub',
            name='club',
            field=models.ForeignKey(to='hockeyapp.Club'),
            preserve_default=True,
        ),
    ]
