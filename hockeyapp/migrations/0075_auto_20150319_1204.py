# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hockeyapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0074_auto_20150317_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='main_color',
            field=models.TextField(default='', help_text='Color hex. Example: #00ffaa', blank=True, verbose_name='Main color', validators=[hockeyapp.models.hex_validator]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='secondary_color',
            field=models.TextField(default='', help_text='Color hex. Example: #00ffaa', blank=True, verbose_name='2th color', validators=[hockeyapp.models.hex_validator]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='third_color',
            field=models.TextField(default='', help_text='Color hex. Example: #00ffaa', blank=True, verbose_name='Third color', validators=[hockeyapp.models.hex_validator]),
            preserve_default=False,
        ),
    ]
