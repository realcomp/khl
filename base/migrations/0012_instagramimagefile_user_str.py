# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_instagramimagefile_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramimagefile',
            name='user_str',
            field=models.CharField(default='', max_length=1024, verbose_name='Instagram user', blank=True),
            preserve_default=False,
        ),
    ]
