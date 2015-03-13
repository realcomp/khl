# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_auto_20150302_1233'),
        ('accounts', '0007_auto_20150312_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='countries',
            field=models.ManyToManyField(to='addresses.Country', verbose_name='Countries'),
            preserve_default=True,
        ),
    ]
