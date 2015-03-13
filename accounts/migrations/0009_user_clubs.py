# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0071_auto_20150313_1636'),
        ('accounts', '0008_user_countries'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='clubs',
            field=models.ManyToManyField(to='hockeyapp.Club', verbose_name='Clubs'),
            preserve_default=True,
        ),
    ]
