# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20141225_0907'),
        ('hockeyapp', '0020_auto_20150114_1101'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arena',
            old_name='capacity',
            new_name='capacity_str',
        ),
        migrations.AddField(
            model_name='arena',
            name='country',
            field=models.ForeignKey(verbose_name='Country', blank=True, to='addresses.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='arena',
            name='league',
            field=models.ForeignKey(blank=True, to='hockeyapp.League', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='arena',
            name='photo',
            field=filer.fields.image.FilerImageField(verbose_name=' Main photo', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
    ]
