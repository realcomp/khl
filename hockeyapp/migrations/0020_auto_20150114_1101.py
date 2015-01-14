# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0019_auto_20150112_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubplayermatch',
            name='pis',
            field=models.FloatField(null=True, verbose_name='Implemented Shots, %'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clubplayermatch',
            name='pis_str',
            field=models.CharField(max_length=8, verbose_name='Implemented Shots, %', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clubplayermatch',
            name='saves_p',
            field=models.FloatField(null=True, verbose_name='Saves Goals , %'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clubplayermatch',
            name='saves_p_str',
            field=models.CharField(max_length=8, verbose_name='Saves Goals , %', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clubplayermatch',
            name='winfaceoff_p',
            field=models.FloatField(null=True, verbose_name='Face-off Wins , %'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clubplayermatch',
            name='winfaceoff_p_str',
            field=models.CharField(max_length=8, verbose_name='Face-off Wins , %', blank=True),
            preserve_default=True,
        ),
    ]
