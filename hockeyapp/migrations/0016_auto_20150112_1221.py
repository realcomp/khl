# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0015_auto_20150111_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='spectators',
            new_name='spectators_str',
        ),
    ]
