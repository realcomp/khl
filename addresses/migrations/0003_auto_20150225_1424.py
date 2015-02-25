# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20141225_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='district',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
    ]
