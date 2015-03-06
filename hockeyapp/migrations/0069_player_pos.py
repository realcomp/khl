# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0068_auto_20150306_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='pos',
            field=models.CharField(default='', max_length=255, verbose_name='Offender position', blank=True),
            preserve_default=False,
        ),
    ]
