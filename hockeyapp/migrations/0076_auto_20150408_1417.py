# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0075_auto_20150319_1204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='height',
            new_name='height_str',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='weight',
            new_name='weight_str',
        ),
    ]
