# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0058_auto_20150225_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Club', blank=True, to='hockeyapp.Club', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timeline',
            name='media_caption',
            field=models.TextField(null=True, verbose_name='Media caption', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timeline',
            name='media_credit',
            field=models.CharField(max_length=255, null=True, verbose_name='Media credit', blank=True),
            preserve_default=True,
        ),
    ]
