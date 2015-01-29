# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0037_auto_20150129_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubplayermatch',
            name='winfaceoff_p',
            field=models.FloatField(null=True, verbose_name='Face-off Wins, %'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clubplayermatch',
            name='winfaceoff_p_str',
            field=models.CharField(max_length=8, verbose_name='Face-off Wins, %', blank=True),
            preserve_default=True,
        ),
    ]
