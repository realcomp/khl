# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0025_auto_20150115_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='line_judges',
            field=models.ManyToManyField(related_name='matchlinejudges', null=True, verbose_name='Line judges', to='hockeyapp.Judge', blank=True),
            preserve_default=True,
        ),
    ]
