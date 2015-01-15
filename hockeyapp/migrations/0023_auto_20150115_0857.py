# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
        ('hockeyapp', '0022_arena_capacity'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArenaPhotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arena', models.ForeignKey(verbose_name='Arena', to='hockeyapp.Arena')),
                ('photo', filer.fields.image.FilerImageField(verbose_name='Photo', to='filer.Image')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='arena',
            name='photo',
            field=filer.fields.image.FilerImageField(verbose_name='Main photo', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
    ]
