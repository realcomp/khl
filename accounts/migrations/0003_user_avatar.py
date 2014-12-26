# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
        ('accounts', '0002_user_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=filer.fields.image.FilerImageField(verbose_name='Avatar', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
    ]
