# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='en_description',
            field=models.TextField(default='', verbose_name='Description (en)', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='ru_description',
            field=models.TextField(verbose_name='Description (rus)', blank=True),
            preserve_default=True,
        ),
    ]
