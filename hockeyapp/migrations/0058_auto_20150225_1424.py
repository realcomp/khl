# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0057_auto_20150225_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='arena',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clubsocial',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coach',
            name='fio',
            field=models.CharField(default='', verbose_name='FIO from parser', max_length=4096, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coachsocial',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judge',
            name='fio',
            field=models.CharField(default='', verbose_name='FIO from parser', max_length=4096, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judgesocial',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='league',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='fio',
            field=models.CharField(default='', verbose_name='FIO from parser', max_length=4096, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playersocial',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schedule',
            name='title',
            field=models.CharField(default='', verbose_name='Title from parser', max_length=1024, editable=False, blank=True),
            preserve_default=False,
        ),
    ]
