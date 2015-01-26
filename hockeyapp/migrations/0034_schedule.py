# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20150116_1503'),
        ('hockeyapp', '0033_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('khl_id', models.PositiveIntegerField(max_length=1024, verbose_name='Other site ID', blank=True)),
                ('date', models.DateTimeField(null=True, verbose_name='Match date', blank=True)),
                ('is_championship', models.BooleanField(default=True, verbose_name='Is championship')),
                ('is_playoff', models.BooleanField(default=False, verbose_name='Is playoff')),
                ('processed', models.BooleanField(default=False)),
                ('proccesed_time', models.DateTimeField(null=True, verbose_name='Processed time', blank=True)),
                ('guest_team', models.ForeignKey(related_name='schedule_guestmatches', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Guest team', blank=True, to='hockeyapp.Club', null=True)),
                ('home_team', models.ForeignKey(related_name='schedule_homematches', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Home team', blank=True, to='hockeyapp.Club', null=True)),
                ('league', models.ForeignKey(blank=True, to='hockeyapp.League', null=True)),
                ('match', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Match')),
                ('season', models.ForeignKey(blank=True, to='base.Season', null=True)),
            ],
            options={
                'ordering': ('date',),
                'verbose_name': 'League Schedule',
                'verbose_name_plural': 'League Schedules',
            },
            bases=(base.models.LocaleAttrMixin, models.Model),
        ),
    ]
