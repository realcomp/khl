# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
        ('hockeyapp', '0029_auto_20150119_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressClubPhotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('addressclub', models.ForeignKey(verbose_name='Club address', to='hockeyapp.AddressClub')),
                ('photo', filer.fields.image.FilerImageField(verbose_name='Photo', to='filer.Image')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='addressclub',
            name='contact_name',
            field=models.CharField(default='', max_length=255, verbose_name='Contact name', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addressclub',
            name='contact_phone',
            field=models.CharField(default='', max_length=255, verbose_name='Contact phone', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addressclub',
            name='contact_post',
            field=models.CharField(default='', max_length=255, verbose_name='Contact post', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addressclub',
            name='coords',
            field=models.CharField(default='', max_length=1024, verbose_name='Latitude and Longitude', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addressclub',
            name='email',
            field=models.EmailField(default='', max_length=75, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addressclub',
            name='office_phone',
            field=models.CharField(default='', max_length=255, verbose_name='Office phone', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addressclub',
            name='phone',
            field=models.CharField(default='', max_length=255, verbose_name='Phone', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addressclub',
            name='photo',
            field=filer.fields.image.FilerImageField(verbose_name='Main photo', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='addressclub',
            name='postaddress',
            field=models.TextField(default='', verbose_name='Post address', blank=True),
            preserve_default=False,
        ),
    ]
