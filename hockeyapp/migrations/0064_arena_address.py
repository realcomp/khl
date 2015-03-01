# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_auto_20150225_1424'),
        ('hockeyapp', '0063_auto_20150227_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='arena',
            name='address',
            field=models.ForeignKey(verbose_name='Address', blank=True, to='addresses.Address', null=True),
            preserve_default=True,
        ),
    ]
