# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0056_clubphotos_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clubphotos',
            options={'ordering': ('photo__created',), 'verbose_name': 'Club instagram photo', 'verbose_name_plural': 'Club instagram photos'},
        ),
    ]
