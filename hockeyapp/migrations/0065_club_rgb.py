# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hockeyapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0064_arena_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='rgb',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='RGB', validators=[hockeyapp.models.rgb_validator]),
            preserve_default=True,
        ),
    ]
