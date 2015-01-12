# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0016_auto_20150112_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='spectators',
            field=models.PositiveIntegerField(null=True, verbose_name='Spectators count'),
            preserve_default=True,
        ),
    ]
