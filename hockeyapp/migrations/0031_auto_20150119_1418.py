# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0030_auto_20150119_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='en_lastname',
            field=models.CharField(max_length=4096, null=True, verbose_name='Last name (en)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coach',
            name='en_name',
            field=models.CharField(max_length=4096, null=True, verbose_name='Name (en)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coach',
            name='ru_lastname',
            field=models.CharField(max_length=4096, null=True, verbose_name='Last name (rus)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coach',
            name='ru_name',
            field=models.CharField(max_length=4096, null=True, verbose_name='Name (rus)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='en_lastname',
            field=models.CharField(max_length=4096, null=True, verbose_name='Last name (en)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='en_name',
            field=models.CharField(max_length=4096, null=True, verbose_name='Name (en)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='ru_lastname',
            field=models.CharField(max_length=4096, null=True, verbose_name='Last name (rus)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='ru_name',
            field=models.CharField(max_length=4096, null=True, verbose_name='Name (rus)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='en_lastname',
            field=models.CharField(max_length=4096, null=True, verbose_name='Last name (en)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='en_name',
            field=models.CharField(max_length=4096, null=True, verbose_name='Name (en)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='ru_lastname',
            field=models.CharField(max_length=4096, null=True, verbose_name='Last name (rus)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='ru_name',
            field=models.CharField(max_length=4096, null=True, verbose_name='Name (rus)', blank=True),
            preserve_default=True,
        ),
    ]
