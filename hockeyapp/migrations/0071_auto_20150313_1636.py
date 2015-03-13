# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0070_auto_20150310_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='parser_type',
            field=models.CharField(blank=True, max_length=255, verbose_name='Parser', choices=[('KHLScheduleParser', 'KHL Schedule Parser'), ('VHLScheduleParser', 'VHL Schedule Parser'), ('MHLScheduleParser', 'MHL Schedule Parser'), ('MHL2ScheduleParser', 'MHL2 Schedule Parser')]),
            preserve_default=True,
        ),
    ]
