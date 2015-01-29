# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0036_auto_20150129_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubplayermatch',
            name='penalty_time',
            field=models.PositiveIntegerField(null=True, verbose_name='Penalty Time'),
            preserve_default=True,
        ),
    ]
