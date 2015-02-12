# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0049_auto_20150212_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='fb',
            field=models.URLField(default='', max_length=1024, verbose_name='Facebook account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='gl',
            field=models.URLField(default='', max_length=1024, verbose_name='Google+ account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='im',
            field=models.URLField(default='', max_length=1024, verbose_name='Instagram account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='ok',
            field=models.URLField(default='', max_length=1024, verbose_name='OK account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='pp',
            field=models.URLField(default='', max_length=1024, verbose_name='Personal page URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='tw',
            field=models.URLField(default='', max_length=1024, verbose_name='Twitter account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='ut',
            field=models.URLField(default='', max_length=1024, verbose_name='Youtube account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='vk',
            field=models.URLField(default='', max_length=1024, verbose_name='VK account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coach',
            name='fb',
            field=models.URLField(default='', max_length=1024, verbose_name='Facebook account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coach',
            name='gl',
            field=models.URLField(default='', max_length=1024, verbose_name='Google+ account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coach',
            name='im',
            field=models.URLField(default='', max_length=1024, verbose_name='Instagram account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coach',
            name='ok',
            field=models.URLField(default='', max_length=1024, verbose_name='OK account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coach',
            name='pp',
            field=models.URLField(default='', max_length=1024, verbose_name='Personal page URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coach',
            name='tw',
            field=models.URLField(default='', max_length=1024, verbose_name='Twitter account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coach',
            name='ut',
            field=models.URLField(default='', max_length=1024, verbose_name='Youtube account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coach',
            name='vk',
            field=models.URLField(default='', max_length=1024, verbose_name='VK account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judge',
            name='fb',
            field=models.URLField(default='', max_length=1024, verbose_name='Facebook account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judge',
            name='gl',
            field=models.URLField(default='', max_length=1024, verbose_name='Google+ account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judge',
            name='im',
            field=models.URLField(default='', max_length=1024, verbose_name='Instagram account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judge',
            name='ok',
            field=models.URLField(default='', max_length=1024, verbose_name='OK account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judge',
            name='pp',
            field=models.URLField(default='', max_length=1024, verbose_name='Personal page URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judge',
            name='tw',
            field=models.URLField(default='', max_length=1024, verbose_name='Twitter account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judge',
            name='ut',
            field=models.URLField(default='', max_length=1024, verbose_name='Youtube account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='judge',
            name='vk',
            field=models.URLField(default='', max_length=1024, verbose_name='VK account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='fb',
            field=models.URLField(default='', max_length=1024, verbose_name='Facebook account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='gl',
            field=models.URLField(default='', max_length=1024, verbose_name='Google+ account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='im',
            field=models.URLField(default='', max_length=1024, verbose_name='Instagram account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='ok',
            field=models.URLField(default='', max_length=1024, verbose_name='OK account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='pp',
            field=models.URLField(default='', max_length=1024, verbose_name='Personal page URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='tw',
            field=models.URLField(default='', max_length=1024, verbose_name='Twitter account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='ut',
            field=models.URLField(default='', max_length=1024, verbose_name='Youtube account URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='vk',
            field=models.URLField(default='', max_length=1024, verbose_name='VK account URL', blank=True),
            preserve_default=False,
        ),
    ]
