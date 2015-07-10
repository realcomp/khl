# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0076_auto_20150408_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='height',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Height'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='weight',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Weight'),
            preserve_default=True,
        ),
    ]
