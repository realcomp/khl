# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('hockeyapp', '0027_club_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressclub',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Season', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clubplayer',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Season', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coachclub',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Season', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leagueclub',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Season', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logoclubhistory',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Season', null=True),
            preserve_default=True,
        ),
    ]
