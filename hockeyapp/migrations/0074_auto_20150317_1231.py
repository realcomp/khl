# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0073_auto_20150316_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='gamingtime_total',
            field=models.IntegerField(null=True, verbose_name='Gaming Time Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='gamingtime_total_index',
            field=models.IntegerField(null=True, verbose_name='Gaming Time Total Index'),
            preserve_default=True,
        ),
    ]
