# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0034_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='khl_id',
            field=models.PositiveIntegerField(null=True, verbose_name='Other site ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='khl_id',
            field=models.PositiveIntegerField(null=True, verbose_name='Other site ID'),
            preserve_default=True,
        ),
    ]
