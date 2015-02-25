# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_auto_20150225_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='socialnetvalue',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='titlealias',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
    ]
