# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0054_timeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubphotos',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Match', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubphotos',
            name='player_numbers',
            field=models.CharField(default='', max_length=1024, blank=True),
            preserve_default=False,
        ),
    ]
