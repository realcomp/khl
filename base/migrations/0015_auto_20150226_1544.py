# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20150225_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instagram_id', models.CharField(max_length=1024, verbose_name='Instagram ID')),
                ('full_name', models.CharField(max_length=1024, verbose_name='Full name', blank=True)),
                ('profile_picture', models.URLField(max_length=1024, verbose_name='Profile picture', blank=True)),
                ('username', models.CharField(max_length=1024, verbose_name='Username', blank=True)),
                ('website', models.URLField(max_length=1024, verbose_name='Website', blank=True)),
                ('bio', models.TextField(verbose_name='BIO', blank=True)),
            ],
            options={
                'verbose_name': 'Instagram user',
                'verbose_name_plural': 'Instagram users',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='instagramimagefile',
            name='instagram_user',
            field=models.ForeignKey(to='base.InstagramUser', null=True),
            preserve_default=True,
        ),
    ]
