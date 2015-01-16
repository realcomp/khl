# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name='Start date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='End date', blank=True)),
            ],
            options={
                'verbose_name': 'Seasons',
            },
            bases=(models.Model,),
        ),
    ]
