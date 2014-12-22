# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
        ('hockeyapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arena',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ru_title', models.CharField(max_length=1024, verbose_name='Title (rus)', blank=True)),
                ('en_title', models.CharField(max_length=1024, verbose_name='Title (en)', blank=True)),
                ('capacity', models.CharField(max_length=1024, verbose_name='Capacity', blank=True)),
                ('site', models.URLField(verbose_name='Site', blank=True)),
                ('contacts', models.TextField(verbose_name='Contacts', blank=True)),
                ('tickets_url', models.URLField(verbose_name='Tickets', blank=True)),
                ('photo', filer.fields.image.FilerImageField(verbose_name='Photo', blank=True, to='filer.Image', null=True)),
            ],
            options={
                'verbose_name': 'Arena',
                'verbose_name_plural': 'Arenas',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='club',
            name='arena',
            field=models.ForeignKey(blank=True, to='hockeyapp.Arena', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='contacts',
            field=models.TextField(default='', verbose_name='Contacts', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='farm_club',
            field=models.OneToOneField(related_name='farmclubparent', null=True, blank=True, to='hockeyapp.Club'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='html_body',
            field=models.TextField(default='', verbose_name='Parse HTML', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='junior_club',
            field=models.OneToOneField(related_name='juniorclubparent', null=True, blank=True, to='hockeyapp.Club'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='proccesed_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 21, 17, 52, 40, 787059, tzinfo=utc), verbose_name='Processed time', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='url',
            field=models.URLField(default='', verbose_name='URL', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='html_body',
            field=models.TextField(default='', verbose_name='Parse HTML', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='proccesed_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 21, 17, 52, 56, 732657, tzinfo=utc), verbose_name='Processed time', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='url',
            field=models.URLField(default='', verbose_name='URL', blank=True),
            preserve_default=False,
        ),
    ]
