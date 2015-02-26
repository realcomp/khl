# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0061_auto_20150226_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arenainstaphoto',
            name='player_numbers',
        ),
        migrations.AddField(
            model_name='arenainstaphoto',
            name='players',
            field=models.ManyToManyField(to='hockeyapp.Player', null=True, blank=True),
            preserve_default=True,
        ),
    ]
