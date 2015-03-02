# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0065_club_rgb'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='assists_average_index',
            field=models.IntegerField(null=True, verbose_name='Assists Average Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='assists_total_index',
            field=models.IntegerField(null=True, verbose_name='Assists Total Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='goals_average_index',
            field=models.IntegerField(null=True, verbose_name='Goals Average Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='goals_total_index',
            field=models.IntegerField(null=True, verbose_name='Goals Total Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='matches_total_index',
            field=models.IntegerField(null=True, verbose_name='Matches Total Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='plus_minus_average_index',
            field=models.IntegerField(null=True, verbose_name='Points Average Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='plus_minus_total_index',
            field=models.IntegerField(null=True, verbose_name='Points Total Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='points_average_index',
            field=models.IntegerField(null=True, verbose_name='Points Average Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='points_total_index',
            field=models.IntegerField(null=True, verbose_name='Points Total Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='seasons_total_index',
            field=models.IntegerField(null=True, verbose_name='Seasons Total Index'),
            preserve_default=True,
        ),
    ]
