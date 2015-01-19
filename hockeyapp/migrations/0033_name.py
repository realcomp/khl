# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0032_auto_20150119_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.SmallIntegerField(choices=[(0, 'First Name'), (1, 'Last Name')])),
                ('ru_name', models.CharField(max_length=4096, verbose_name='Name (rus)', blank=True)),
                ('en_name', models.CharField(max_length=4096, verbose_name='Name (en)', blank=True)),
            ],
            options={
                'verbose_name': 'Name',
                'verbose_name_plural': 'Names',
            },
            bases=(models.Model,),
        ),
    ]
