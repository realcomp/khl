# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='version',
            field=models.CharField(default='CLASSIC', max_length=8, verbose_name='Account version', choices=[(b'CLASSIC', 'Classic version'), (b'PRO', 'Pro version')]),
            preserve_default=True,
        ),
    ]
