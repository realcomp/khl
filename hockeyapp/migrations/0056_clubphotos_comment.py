# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0055_auto_20150220_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubphotos',
            name='comment',
            field=models.CharField(default='', max_length=1024, verbose_name='Comment', blank=True),
            preserve_default=False,
        ),
    ]
