# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_auto_20150225_1424'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ('ru_title', 'en_title', 'title', 'pk'), 'verbose_name': 'Address', 'verbose_name_plural': 'Addresses'},
        ),
    ]
