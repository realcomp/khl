# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20150225_1424'),
        ('hockeyapp', '0060_auto_20150226_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArenaInstaPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player_numbers', models.CharField(max_length=1024, blank=True)),
                ('comment', models.CharField(max_length=1024, verbose_name='Comment', blank=True)),
                ('processed', models.BooleanField(default=False)),
                ('proccesed_time', models.DateTimeField(auto_now=True, verbose_name='Processed time')),
                ('arena', models.ForeignKey(verbose_name='Arena', to='hockeyapp.Arena')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Club', null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Match', null=True)),
                ('photo', models.ForeignKey(to='base.InstagramImageFile')),
            ],
            options={
                'ordering': ('photo__created',),
                'verbose_name': 'Club instagram photo',
                'verbose_name_plural': 'Club instagram photos',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='arenainstagram',
            name='arena',
        ),
        migrations.DeleteModel(
            name='ArenaInstagram',
        ),
        migrations.RemoveField(
            model_name='clubphotos',
            name='club',
        ),
        migrations.RemoveField(
            model_name='clubphotos',
            name='match',
        ),
        migrations.RemoveField(
            model_name='clubphotos',
            name='photo',
        ),
        migrations.DeleteModel(
            name='ClubPhotos',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='bullet_goals_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='es_goals_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='ev_goals_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='faceoff_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='gamingtime_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='loose_goals_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='overtime_goals_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='penalty_time_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='pis_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='plus_minus_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='pp_goals_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='saves_p_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='saves_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='sf_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='shots_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='win_goals_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='winfaceoff_p_str',
        ),
        migrations.RemoveField(
            model_name='clubplayermatch',
            name='winfaceoff_str',
        ),
        migrations.RemoveField(
            model_name='match',
            name='is_championship',
        ),
        migrations.RemoveField(
            model_name='match',
            name='is_playoff',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='is_championship',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='is_playoff',
        ),
    ]
