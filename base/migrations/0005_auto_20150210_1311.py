# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_socialnetvalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialnetvalue',
            name='stype',
            field=models.PositiveIntegerField(null=True, verbose_name='Social Network', choices=[(1, 'VK'), (2, 'OK'), (3, 'Facebook'), (4, 'Goggle+'), (5, 'Twitter'), (6, 'Instagram')]),
            preserve_default=True,
        ),
    ]
