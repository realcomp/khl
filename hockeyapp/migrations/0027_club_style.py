# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0026_auto_20150116_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='style',
            field=models.TextField(null=True, verbose_name='Styles (CSS)', blank=True),
            preserve_default=True,
        ),
    ]
