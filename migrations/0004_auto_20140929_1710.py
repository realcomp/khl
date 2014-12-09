# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20140925_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uin',
            field=models.CharField(unique=True, max_length=255, verbose_name=b'UIN', blank=True),
        ),
    ]
