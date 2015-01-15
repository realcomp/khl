# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0023_auto_20150115_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='arena',
            name='coords',
            field=models.CharField(default='', max_length=1024, verbose_name='Latitude and Longitude', blank=True),
            preserve_default=False,
        ),
    ]
