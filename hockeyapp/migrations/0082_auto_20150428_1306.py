# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0081_auto_20150423_1430'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relatedplayer',
            options={'ordering': ('modified',), 'verbose_name': 'Related Player', 'verbose_name_plural': 'Related Players'},
        ),
        migrations.AddField(
            model_name='player',
            name='last_relatedplayer_modified',
            field=models.DateTimeField(null=True, verbose_name='Last related player modified date'),
            preserve_default=True,
        ),
    ]
