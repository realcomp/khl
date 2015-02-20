# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_instagramimagefile_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramimagefile',
            name='comment',
            field=models.CharField(default='', max_length=1024, verbose_name='Comment', blank=True),
            preserve_default=False,
        ),
    ]
