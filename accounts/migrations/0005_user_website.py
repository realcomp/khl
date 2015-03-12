# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_name_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.URLField(max_length=1024, verbose_name='Website', blank=True),
            preserve_default=True,
        ),
    ]
