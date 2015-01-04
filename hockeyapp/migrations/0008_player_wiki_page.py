# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0007_auto_20150104_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='wiki_page',
            field=models.URLField(default='', verbose_name='Wiki page URL', blank=True),
            preserve_default=False,
        ),
    ]
