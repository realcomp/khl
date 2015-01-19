# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0028_auto_20150116_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='coaches',
            field=models.ManyToManyField(related_name='helpcoachclubs', null=True, verbose_name='Help coaches', to='hockeyapp.Coach', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='coach',
            field=models.ForeignKey(related_name='headcoachclubs', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Head Coach', blank=True, to='hockeyapp.Coach', null=True),
            preserve_default=True,
        ),
    ]
