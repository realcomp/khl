# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20141125_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uin',
            field=models.CharField(max_length=255, verbose_name=b'UIN', blank=True),
        ),
    ]
