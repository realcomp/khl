# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20150226_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramimagefile',
            name='user_str',
            field=models.CharField(max_length=1024, verbose_name='Instagram username', blank=True),
            preserve_default=True,
        ),
    ]
