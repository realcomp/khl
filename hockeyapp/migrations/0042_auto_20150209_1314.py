# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0041_clubtitlealias'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='assists_average',
            field=models.IntegerField(null=True, verbose_name='Assists Average'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='assists_total',
            field=models.IntegerField(null=True, verbose_name='Assists Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='goals_average',
            field=models.IntegerField(null=True, verbose_name='Goals Average'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='goals_total',
            field=models.IntegerField(null=True, verbose_name='Goals Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='plus_minus_average',
            field=models.IntegerField(null=True, verbose_name='Points Average'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='plus_minus_total',
            field=models.IntegerField(null=True, verbose_name='Points Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='points_average',
            field=models.IntegerField(null=True, verbose_name='Points Average'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='points_total',
            field=models.IntegerField(null=True, verbose_name='Points Total'),
            preserve_default=True,
        ),
    ]
