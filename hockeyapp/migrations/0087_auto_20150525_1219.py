# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0086_auto_20150522_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='pis_average',
            field=models.FloatField(null=True, verbose_name='% Implemented Shots Average'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='shots_total',
            field=models.IntegerField(null=True, verbose_name='Shots Count Total'),
            preserve_default=True,
        ),
    ]
