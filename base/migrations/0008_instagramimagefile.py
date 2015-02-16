# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0001_initial'),
        ('base', '0007_auto_20150212_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramImageFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instagram_id', models.CharField(max_length=1024, verbose_name='Instagram ID')),
                ('link', models.URLField(verbose_name='Link')),
                ('data', jsonfield.fields.JSONField()),
                ('img', filer.fields.image.FilerImageField(verbose_name='Photo', to='filer.Image')),
            ],
            options={
                'verbose_name': 'Instagram image file',
                'verbose_name_plural': 'Instagram image files',
            },
            bases=(models.Model,),
        ),
    ]
