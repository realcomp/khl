# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0079_auto_20150414_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField(verbose_name='Similarity value')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('player1', models.ForeignKey(related_name='relatedplayers1', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Player 1', blank=True, to='hockeyapp.Player', null=True)),
                ('player2', models.ForeignKey(related_name='relatedplayers2', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Player 2', blank=True, to='hockeyapp.Player', null=True)),
            ],
            options={
                'verbose_name': 'Related Player',
                'verbose_name_plural': 'Related Players',
            },
            bases=(models.Model,),
        ),
    ]
