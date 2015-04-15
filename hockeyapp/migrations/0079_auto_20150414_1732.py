# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0078_auto_20150410_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='bullet_win',
            field=models.BooleanField(default=False, verbose_name='Bullets'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='guest_score',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Guest score'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='home_score',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Home score'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='overtime_win',
            field=models.BooleanField(default=False, verbose_name='Overtime'),
            preserve_default=True,
        ),
    ]
