# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name_visible',
            field=models.BooleanField(default=True, verbose_name='Name visible'),
            preserve_default=True,
        ),
    ]
