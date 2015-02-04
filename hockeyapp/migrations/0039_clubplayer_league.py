# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0038_auto_20150129_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubplayer',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.League', null=True),
            preserve_default=True,
        ),
    ]
