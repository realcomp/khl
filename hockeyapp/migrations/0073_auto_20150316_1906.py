# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0072_auto_20150316_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='matches_lose_total',
            field=models.IntegerField(null=True, verbose_name='Matches Lose Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='matches_lose_total_index',
            field=models.IntegerField(null=True, verbose_name='Matches Lose Total Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='matches_win_total',
            field=models.IntegerField(null=True, verbose_name='Matches Win Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='matches_win_total_index',
            field=models.IntegerField(null=True, verbose_name='Matches Win Total Index'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='sf_average_index',
            field=models.IntegerField(null=True, verbose_name='Safety Factor Average Index'),
            preserve_default=True,
        ),
    ]
