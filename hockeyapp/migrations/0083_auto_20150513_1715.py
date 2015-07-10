# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0082_auto_20150428_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='last_match_date',
            field=models.DateTimeField(null=True, verbose_name='Last match history parsed'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='matches_total',
            field=models.IntegerField(null=True, verbose_name='Matches Total'),
            preserve_default=True,
        ),
    ]
