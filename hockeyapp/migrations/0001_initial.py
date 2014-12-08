# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractMan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fio', models.CharField(max_length=4096, verbose_name=b'\xd0\xa4\xd0\x98\xd0\x9e', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('abstractman_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hockeyapp.AbstractMan')),
            ],
            options={
                'verbose_name': '\u0422\u0440\u0435\u043d\u0435\u0440',
                'verbose_name_plural': '\u0422\u0440\u0435\u043d\u0435\u0440\u044b',
            },
            bases=('hockeyapp.abstractman',),
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('abstractman_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hockeyapp.AbstractMan')),
            ],
            options={
                'verbose_name': '\u0421\u0443\u0434\u044c\u044f',
                'verbose_name_plural': '\u0421\u0443\u0434\u044c\u0438',
            },
            bases=('hockeyapp.abstractman',),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1024, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', blank=True)),
                ('khl_id', models.PositiveIntegerField(max_length=1024, verbose_name=b'ID \xd0\xbd\xd0\xb0 \xd1\x81\xd1\x82\xd0\xbe\xd1\x80\xd0\xbe\xd0\xbd\xd0\xbd\xd0\xb5\xd0\xbc \xd1\x80\xd0\xb5\xd1\x81\xd1\x83\xd1\x80\xd1\x81\xd0\xb5', blank=True)),
                ('proccesed_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xd0\x9e\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xb0\xd0\xbd, \xd0\xb2\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f')),
                ('spectators', models.CharField(max_length=1024, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x81\xd0\xb5\xd1\x89\xd0\xb0\xd0\xb5\xd0\xbc\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c', blank=True)),
                ('date', models.CharField(max_length=1024, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbc\xd0\xb0\xd1\x82\xd1\x87\xd0\xb0', blank=True)),
                ('count', models.CharField(max_length=1024, verbose_name=b'\xd0\xa1\xd1\x87\xd0\xb5\xd1\x82 \xd0\xbc\xd0\xb0\xd1\x82\xd1\x87\xd0\xb0', blank=True)),
                ('detail_count', models.CharField(max_length=1024, verbose_name=b'\xd0\xa1\xd1\x87\xd0\xb5\xd1\x82 \xd0\xbf\xd0\xbe \xd0\xbf\xd0\xb5\xd1\x80\xd0\xb8\xd0\xbe\xd0\xb4\xd0\xb0\xd0\xbc', blank=True)),
            ],
            options={
                'ordering': ('-khl_id',),
                'verbose_name': '\u041c\u0430\u0442\u0447',
                'verbose_name_plural': '\u041c\u0430\u0442\u0447\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('abstractman_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hockeyapp.AbstractMan')),
            ],
            options={
                'verbose_name': '\u0418\u0433\u0440\u043e\u043a',
                'verbose_name_plural': '\u0418\u0433\u0440\u043e\u043a\u0438',
            },
            bases=('hockeyapp.abstractman',),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1024, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', blank=True)),
                ('coach', models.ForeignKey(blank=True, to='hockeyapp.Coach', null=True)),
                ('players', models.ManyToManyField(to='hockeyapp.Player', null=True, blank=True)),
                ('region', models.ForeignKey(blank=True, to='base.Region', null=True)),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043c\u0430\u043d\u0434\u0430',
                'verbose_name_plural': '\u041a\u043e\u043c\u0430\u043d\u0434\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='match',
            name='guest_team',
            field=models.ForeignKey(related_name='guestteam', verbose_name=b'\xd0\x93\xd0\xbe\xd1\x81\xd1\x82\xd0\xb5\xd0\xb2\xd0\xb0\xd1\x8f \xd0\xba\xd0\xbe\xd0\xbc\xd0\xb0\xd0\xbd\xd0\xb4\xd0\xb0', blank=True, to='hockeyapp.Team', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='home_team',
            field=models.ForeignKey(related_name='hometeam', verbose_name=b'\xd0\x94\xd0\xbe\xd0\xbc\xd0\xb0\xd1\x88\xd0\xbd\xd1\x8f\xd1\x8f \xd0\xba\xd0\xbe\xd0\xbc\xd0\xb0\xd0\xbd\xd0\xb4\xd0\xb0', blank=True, to='hockeyapp.Team', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='judges',
            field=models.ManyToManyField(related_name='matchjudges', null=True, verbose_name=b'\xd0\xa1\xd1\x83\xd0\xb4\xd1\x8c\xd0\xb8', to='hockeyapp.Judge', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='line_judges',
            field=models.ManyToManyField(related_name='matchllinejudges', null=True, verbose_name=b'\xd0\x9b\xd0\xb8\xd0\xbd\xd0\xb5\xd0\xb9\xd0\xbd\xd1\x8b\xd0\xb5 \xd1\x81\xd1\x83\xd0\xb4\xd1\x8c\xd0\xb8', to='hockeyapp.Judge', blank=True),
            preserve_default=True,
        ),
    ]
