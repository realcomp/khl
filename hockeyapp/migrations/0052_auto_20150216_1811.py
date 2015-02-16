# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0051_auto_20150213_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='assists_average',
            field=models.FloatField(null=True, verbose_name='Assists Average'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='goals_average',
            field=models.FloatField(null=True, verbose_name='Goals Average'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='plus_minus_average',
            field=models.FloatField(null=True, verbose_name='Points Average'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='points_average',
            field=models.FloatField(null=True, verbose_name='Points Average'),
            preserve_default=True,
        ),
    ]
