# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0008_player_wiki_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='wiki_page',
            field=models.URLField(max_length=1024, verbose_name='Wiki page URL', blank=True),
            preserve_default=True,
        ),
    ]
