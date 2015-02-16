# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_instagramimagefile'),
        ('hockeyapp', '0050_auto_20150212_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArenaInstagram',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, verbose_name='Name')),
                ('im_id', models.CharField(max_length=1024, verbose_name='Instagram ID')),
                ('lat', models.CharField(max_length=1024, verbose_name='Latitude')),
                ('lng', models.CharField(max_length=1024, verbose_name='Longtitude')),
                ('arena', models.ForeignKey(to='hockeyapp.Arena')),
            ],
            options={
                'verbose_name': 'Arena instagram',
                'verbose_name_plural': 'Arena instagrams',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClubPhotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('club', models.ForeignKey(verbose_name='Club', to='hockeyapp.Club')),
                ('photo', models.ForeignKey(to='base.InstagramImageFile')),
            ],
            options={
                'verbose_name': 'Club instagram photo',
                'verbose_name_plural': 'Club instagram photos',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='arena',
            name='capacity_str',
        ),
    ]
