# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_notification',
            field=models.BooleanField(default=True, verbose_name='E-mail notification'),
            preserve_default=True,
        ),
    ]
