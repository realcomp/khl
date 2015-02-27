# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0062_auto_20150226_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeline',
            name='media_caption',
        ),
        migrations.RemoveField(
            model_name='timeline',
            name='media_credit',
        ),
        migrations.AddField(
            model_name='timeline',
            name='en_media_caption',
            field=models.CharField(max_length=255, null=True, verbose_name='Media caption (EN)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timeline',
            name='en_media_credit',
            field=models.CharField(max_length=255, null=True, verbose_name='Media credit (EN)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timeline',
            name='ru_media_caption',
            field=models.CharField(max_length=255, null=True, verbose_name='Media caption (RU)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timeline',
            name='ru_media_credit',
            field=models.CharField(max_length=255, null=True, verbose_name='Media credit (RU)', blank=True),
            preserve_default=True,
        ),
    ]
