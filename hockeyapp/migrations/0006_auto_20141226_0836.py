# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20141225_0907'),
        ('hockeyapp', '0005_auto_20141224_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='addresses.Country', null=True)),
            ],
            options={
                'verbose_name': 'League',
                'verbose_name_plural': 'Leagues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LeagueClub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='Start date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='End date', blank=True)),
                ('club', models.ForeignKey(to='hockeyapp.Club')),
                ('league', models.ForeignKey(to='hockeyapp.League')),
            ],
            options={
                'verbose_name': 'Club league',
                'verbose_name_plural': 'Club leagues',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='club',
            name='league',
            field=models.ForeignKey(blank=True, to='hockeyapp.League', null=True),
            preserve_default=True,
        ),
    ]
