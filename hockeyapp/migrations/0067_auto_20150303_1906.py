# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0066_auto_20150302_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='penalty_time_average',
            field=models.FloatField(null=True, verbose_name='Penalty Time Average'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='penalty_time_average_index',
            field=models.IntegerField(null=True, verbose_name='Penalty Time Average Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='penalty_time_total',
            field=models.IntegerField(null=True, verbose_name='Penalty Time Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='penalty_time_total_index',
            field=models.IntegerField(null=True, verbose_name='Penalty Time Total Index'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='plus_minus_average',
            field=models.FloatField(null=True, verbose_name='Plus/minus Average'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='plus_minus_average_index',
            field=models.IntegerField(null=True, verbose_name='Plus/minus Average Index'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='plus_minus_total',
            field=models.IntegerField(null=True, verbose_name='Plus/minus Total'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='plus_minus_total_index',
            field=models.IntegerField(null=True, verbose_name='Plus/minus Total Index'),
            preserve_default=True,
        ),
    ]
