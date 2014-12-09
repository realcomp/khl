# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20140929_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='imei',
            field=models.CharField(default='', max_length=16, verbose_name=b'IMEI', blank=True),
            preserve_default=False,
        ),
    ]
