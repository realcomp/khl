# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20150216_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramimagefile',
            name='created',
            field=models.DateTimeField(null=True, verbose_name='Created date', blank=True),
            preserve_default=True,
        ),
    ]
