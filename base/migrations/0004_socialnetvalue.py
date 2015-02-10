# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_titlealias'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialNetValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('stype', models.PositiveIntegerField(null=True, verbose_name='Social Network', choices=[(1, 'VK'), (2, 'OK'), (3, 'Facebook'), (4, 'Goggle+'), (5, 'Twitter'), (6, 'Instagramm')])),
            ],
            options={
                'verbose_name': 'Social Network Value',
                'verbose_name_plural': 'Social Network Values',
            },
            bases=(base.models.LocaleAttrMixin, models.Model),
        ),
    ]
