# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_user_clubs'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_validated',
            field=models.BooleanField(default=False, verbose_name='E-mail validated'),
            preserve_default=True,
        ),
    ]
