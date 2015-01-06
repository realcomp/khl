# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20141225_0907'),
        ('filer', '__first__'),
        ('hockeyapp', '0009_auto_20150104_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='Birth date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coach',
            name='citizenship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Citizenship', blank=True, to='addresses.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coach',
            name='death_date',
            field=models.DateField(null=True, verbose_name='Death date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coach',
            name='photo',
            field=filer.fields.image.FilerImageField(verbose_name='Photo', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coach',
            name='wiki_page',
            field=models.URLField(default='', max_length=1024, verbose_name='Wiki page URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judge',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='Birth date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='citizenship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Citizenship', blank=True, to='addresses.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='death_date',
            field=models.DateField(null=True, verbose_name='Death date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='photo',
            field=filer.fields.image.FilerImageField(verbose_name='Photo', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='wiki_page',
            field=models.URLField(default='', max_length=1024, verbose_name='Wiki page URL', blank=True),
            preserve_default=False,
        ),
    ]
