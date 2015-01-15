# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0021_auto_20150115_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='arena',
            name='capacity',
            field=models.PositiveIntegerField(null=True, verbose_name='Capacity'),
            preserve_default=True,
        ),
    ]
