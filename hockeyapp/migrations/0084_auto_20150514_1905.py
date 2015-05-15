# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0083_auto_20150513_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='guest_count',
            field=models.IntegerField(default=0, verbose_name='Guest team count'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='home_count',
            field=models.IntegerField(default=0, verbose_name='Home team count'),
            preserve_default=True,
        ),
    ]
