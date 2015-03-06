# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0067_auto_20150303_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='birth_place',
            field=models.CharField(default='', max_length=255, verbose_name='Birth place', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='first_school',
            field=models.CharField(default='', max_length=255, verbose_name='First school', blank=True),
            preserve_default=False,
        ),
    ]
