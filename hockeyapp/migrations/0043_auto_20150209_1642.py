# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0042_auto_20150209_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='matches_total',
            field=models.IntegerField(null=True, verbose_name='Matches Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='seasons_total',
            field=models.IntegerField(null=True, verbose_name='Seasons Total'),
            preserve_default=True,
        ),
    ]
