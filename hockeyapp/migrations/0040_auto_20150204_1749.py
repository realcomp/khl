# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0039_clubplayer_league'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='is_championship',
            field=models.BooleanField(default=True, verbose_name='Is championship'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='is_playoff',
            field=models.BooleanField(default=False, verbose_name='Is playoff'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='proccesed_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Processed time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='proccesed_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Processed time', null=True),
            preserve_default=True,
        ),
    ]
