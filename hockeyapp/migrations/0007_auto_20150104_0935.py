# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20141225_0907'),
        ('hockeyapp', '0006_auto_20141226_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='citizenship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Citizenship', blank=True, to='addresses.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='contract_to',
            field=models.DateField(null=True, verbose_name='Contract to', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='contract_type',
            field=models.CharField(default='', max_length=32, verbose_name='Contract type', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='death_date',
            field=models.DateField(null=True, verbose_name='Death date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='grip',
            field=models.CharField(default='', max_length=32, verbose_name='Grip', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='number',
            field=models.CharField(default='', max_length=32, verbose_name='Number', blank=True),
            preserve_default=False,
        ),
    ]
