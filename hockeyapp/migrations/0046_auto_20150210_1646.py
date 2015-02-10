# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0045_auto_20150210_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='challenge_type',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Challenge Type', choices=[(0, 'unknown'), (1, 'Championship'), (2, 'Playoff'), (3, 'Hopeful cup'), (4, 'Junior World Cup'), (5, 'Challenge Cup'), (6, 'MHL playout'), (7, 'MHL qualifying tournament'), (8, 'MHL-2 Generation Cup')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schedule',
            name='challenge_type',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Challenge Type', choices=[(0, 'unknown'), (1, 'Championship'), (2, 'Playoff'), (3, 'Hopeful cup'), (4, 'Junior World Cup'), (5, 'Challenge Cup'), (6, 'MHL playout'), (7, 'MHL qualifying tournament'), (8, 'MHL-2 Generation Cup')]),
            preserve_default=True,
        ),
    ]
