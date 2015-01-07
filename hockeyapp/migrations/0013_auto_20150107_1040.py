# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0012_auto_20150107_1030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='date',
            new_name='date_str',
        ),
        migrations.AddField(
            model_name='match',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='Match date', blank=True),
            preserve_default=True,
        ),
    ]
