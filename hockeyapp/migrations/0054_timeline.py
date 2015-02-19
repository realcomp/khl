# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.db.models.deletion
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0001_initial'),
        ('hockeyapp', '0053_auto_20150217_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(null=True, verbose_name='Start date', blank=True)),
                ('end_date', models.DateTimeField(null=True, verbose_name='End date', blank=True)),
                ('ru_headline', models.CharField(max_length=255, null=True, verbose_name='Headline (RU)', blank=True)),
                ('en_headline', models.CharField(max_length=255, null=True, verbose_name='Headline (EN)', blank=True)),
                ('ru_text', models.TextField(null=True, verbose_name='Text (RU)', blank=True)),
                ('en_text', models.TextField(null=True, verbose_name='Text (EN)', blank=True)),
                ('type', models.CharField(max_length=255, null=True, verbose_name='Type', blank=True)),
                ('tag', models.CharField(max_length=255, null=True, verbose_name='Tag', blank=True)),
                ('media', filer.fields.image.FilerImageField(verbose_name='Media', blank=True, to='filer.Image', null=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Player', blank=True, to='hockeyapp.Player', null=True)),
            ],
            options={
                'ordering': ('start_date',),
                'verbose_name': 'Timeline event',
                'verbose_name_plural': 'Timeline events',
            },
            bases=(base.models.LocaleAttrMixin, models.Model),
        ),
    ]
