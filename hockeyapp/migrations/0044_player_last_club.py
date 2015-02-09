# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0043_auto_20150209_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='last_club',
            field=models.ForeignKey(related_name='last_players', verbose_name='Club', to='hockeyapp.Club', null=True),
            preserve_default=True,
        ),
    ]
