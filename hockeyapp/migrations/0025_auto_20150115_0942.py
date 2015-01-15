# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0024_arena_coords'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='khl_id',
            field=models.PositiveIntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='khl_id',
            field=models.PositiveIntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='khl_id',
            field=models.PositiveIntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
