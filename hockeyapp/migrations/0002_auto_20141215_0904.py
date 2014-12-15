# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='addressclub',
            options={'verbose_name': 'Club address', 'verbose_name_plural': 'Club addresses'},
        ),
        migrations.AlterModelOptions(
            name='clubplayer',
            options={'verbose_name': 'Club player', 'verbose_name_plural': 'Club players'},
        ),
        migrations.AlterModelOptions(
            name='coachclub',
            options={'verbose_name': 'Club coach', 'verbose_name_plural': 'Club coaches'},
        ),
        migrations.AlterModelOptions(
            name='matchgoalhistory',
            options={'verbose_name': 'Match goal entry', 'verbose_name_plural': 'Match goal entries'},
        ),
        migrations.AlterModelOptions(
            name='matchpenaltyhistory',
            options={'verbose_name': 'Match penalty entry', 'verbose_name_plural': 'Match penalty entries'},
        ),
        migrations.AddField(
            model_name='matchgoalhistory',
            name='guest_five_numbers',
            field=models.CharField(default='', max_length=1024, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addressclub',
            name='end_date',
            field=models.DateField(null=True, verbose_name='End date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='addressclub',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Start date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='closing_dt',
            field=models.DateField(null=True, verbose_name='Closing date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='opening_dt',
            field=models.DateField(null=True, verbose_name='Founding date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clubplayer',
            name='end_date',
            field=models.DateField(null=True, verbose_name='End date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clubplayer',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Start date', blank=True),
            preserve_default=True,
        ),
    ]
