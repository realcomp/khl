# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1024, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', blank=True)),
            ],
            options={
                'verbose_name': '\u0420\u0435\u0433\u0438\u043e\u043d',
                'verbose_name_plural': '\u0420\u0435\u0433\u0438\u043e\u043d\u044b',
            },
            bases=(models.Model,),
        ),
    ]
