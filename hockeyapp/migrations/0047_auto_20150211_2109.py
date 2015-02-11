# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20150210_1314'),
        ('hockeyapp', '0046_auto_20150210_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerCoachJudge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coach', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Coach', verbose_name='Coach')),
                ('judge', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Judge', verbose_name='Judge')),
                ('player', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Player', verbose_name='Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='club',
            name='socials',
            field=models.ManyToManyField(to='base.SocialNetValue', null=True, verbose_name='Social accounts', blank=True),
            preserve_default=True,
        ),
    ]
