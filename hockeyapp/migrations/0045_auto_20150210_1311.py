# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20150210_1311'),
        ('hockeyapp', '0044_player_last_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='socials',
            field=models.ManyToManyField(to='base.SocialNetValue', null=True, verbose_name='Social accounts', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='judge',
            name='socials',
            field=models.ManyToManyField(to='base.SocialNetValue', null=True, verbose_name='Social accounts', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='socials',
            field=models.ManyToManyField(to='base.SocialNetValue', null=True, verbose_name='Social accounts', blank=True),
            preserve_default=True,
        ),
    ]
