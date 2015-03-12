# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_email_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sport_basketball',
            field=models.BooleanField(default=False, verbose_name='Fav. basketball'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='sport_football',
            field=models.BooleanField(default=False, verbose_name='Fav. football'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='sport_hockey',
            field=models.BooleanField(default=False, verbose_name='Fav. hockey'),
            preserve_default=True,
        ),
    ]
