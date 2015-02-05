# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20150116_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='TitleAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
            ],
            options={
                'verbose_name': 'Title alias',
                'verbose_name_plural': 'Title aliases',
            },
            bases=(base.models.LocaleAttrMixin, models.Model),
        ),
    ]
