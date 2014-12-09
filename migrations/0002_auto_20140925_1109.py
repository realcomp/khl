# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-date_joined',)},
        ),
        migrations.AddField(
            model_name='user',
            name='fio',
            field=models.CharField(default='', max_length=1024, verbose_name=b'\xd0\xa4\xd0\x98\xd0\x9e'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb4\xd1\x82\xd0\xb2\xd0\xb5\xd1\x80\xd0\xb6\xd0\xb4\xd0\xb5\xd0\xbd\xd0\xbd\xd1\x8b\xd0\xb9'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='org',
            field=models.CharField(default='', max_length=255, verbose_name=b'\xd0\x9e\xd1\x80\xd0\xb3\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=255, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd', blank=True),
            preserve_default=False,
        ),
    ]
