# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0035_auto_20150127_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubplayermatch',
            name='assists',
            field=models.SmallIntegerField(null=True, verbose_name='Assists'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='blocks',
            field=models.PositiveIntegerField(null=True, verbose_name='Blocks'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='change_count',
            field=models.PositiveIntegerField(null=True, verbose_name='Change count'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='fouls',
            field=models.PositiveIntegerField(null=True, verbose_name='Fouls'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='goals',
            field=models.SmallIntegerField(null=True, verbose_name='Goals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='hits',
            field=models.PositiveIntegerField(null=True, verbose_name='Hits'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayermatch',
            name='points',
            field=models.SmallIntegerField(null=True, verbose_name='Points'),
            preserve_default=True,
        ),
    ]
