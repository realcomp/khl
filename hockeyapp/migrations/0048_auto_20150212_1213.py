# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0047_auto_20150211_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('stype', models.PositiveIntegerField(null=True, verbose_name='Social Network', choices=[(1, 'VK'), (2, 'OK'), (3, 'Facebook'), (4, 'Goggle+'), (5, 'Twitter'), (6, 'Instagram'), (7, 'Personal page')])),
                ('club', models.ForeignKey(to='hockeyapp.Club')),
            ],
            options={
                'verbose_name': 'Club social account',
                'verbose_name_plural': 'Clubs social accounts',
            },
            bases=(base.models.LocaleAttrMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CoachSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('stype', models.PositiveIntegerField(null=True, verbose_name='Social Network', choices=[(1, 'VK'), (2, 'OK'), (3, 'Facebook'), (4, 'Goggle+'), (5, 'Twitter'), (6, 'Instagram'), (7, 'Personal page')])),
                ('coach', models.ForeignKey(to='hockeyapp.Coach')),
            ],
            options={
                'verbose_name': 'Coach social account',
                'verbose_name_plural': 'Coaches social accounts',
            },
            bases=(base.models.LocaleAttrMixin, models.Model),
        ),
        migrations.CreateModel(
            name='JudgeSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('stype', models.PositiveIntegerField(null=True, verbose_name='Social Network', choices=[(1, 'VK'), (2, 'OK'), (3, 'Facebook'), (4, 'Goggle+'), (5, 'Twitter'), (6, 'Instagram'), (7, 'Personal page')])),
                ('judge', models.ForeignKey(to='hockeyapp.Judge')),
            ],
            options={
                'verbose_name': 'Judge social account',
                'verbose_name_plural': 'Judges social accounts',
            },
            bases=(base.models.LocaleAttrMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PlayerSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('stype', models.PositiveIntegerField(null=True, verbose_name='Social Network', choices=[(1, 'VK'), (2, 'OK'), (3, 'Facebook'), (4, 'Goggle+'), (5, 'Twitter'), (6, 'Instagram'), (7, 'Personal page')])),
                ('player', models.ForeignKey(to='hockeyapp.Player')),
            ],
            options={
                'verbose_name': 'Player social account',
                'verbose_name_plural': 'Players social accounts',
            },
            bases=(base.models.LocaleAttrMixin, models.Model),
        ),
        migrations.AlterModelOptions(
            name='playercoachjudge',
            options={'verbose_name': 'Player - Coach - Judge', 'verbose_name_plural': 'Player - Coach - Judge'},
        ),
        migrations.RemoveField(
            model_name='club',
            name='socials',
        ),
        migrations.RemoveField(
            model_name='coach',
            name='socials',
        ),
        migrations.RemoveField(
            model_name='judge',
            name='socials',
        ),
        migrations.RemoveField(
            model_name='player',
            name='socials',
        ),
    ]
