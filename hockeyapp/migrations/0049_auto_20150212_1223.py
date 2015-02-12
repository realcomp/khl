# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0048_auto_20150212_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubsocial',
            name='stype',
            field=models.PositiveIntegerField(null=True, verbose_name='Social Network', choices=[(1, 'VK'), (2, 'OK'), (3, 'Facebook'), (4, 'Goggle+'), (5, 'Twitter'), (6, 'Instagram'), (7, 'Personal page'), (8, 'Youtube')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coachsocial',
            name='stype',
            field=models.PositiveIntegerField(null=True, verbose_name='Social Network', choices=[(1, 'VK'), (2, 'OK'), (3, 'Facebook'), (4, 'Goggle+'), (5, 'Twitter'), (6, 'Instagram'), (7, 'Personal page'), (8, 'Youtube')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='judgesocial',
            name='stype',
            field=models.PositiveIntegerField(null=True, verbose_name='Social Network', choices=[(1, 'VK'), (2, 'OK'), (3, 'Facebook'), (4, 'Goggle+'), (5, 'Twitter'), (6, 'Instagram'), (7, 'Personal page'), (8, 'Youtube')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='playersocial',
            name='stype',
            field=models.PositiveIntegerField(null=True, verbose_name='Social Network', choices=[(1, 'VK'), (2, 'OK'), (3, 'Facebook'), (4, 'Goggle+'), (5, 'Twitter'), (6, 'Instagram'), (7, 'Personal page'), (8, 'Youtube')]),
            preserve_default=True,
        ),
    ]
