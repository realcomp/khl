# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0071_auto_20150313_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='bullet_matches_total',
            field=models.IntegerField(null=True, verbose_name='Total Matches with Bullet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='bullet_matches_total_index',
            field=models.IntegerField(null=True, verbose_name='Total Matches with Bullet Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='loose_goals_total',
            field=models.IntegerField(null=True, verbose_name='Loose Goals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='loose_goals_total_index',
            field=models.IntegerField(null=True, verbose_name='Loose Goals Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='saves_p_average',
            field=models.FloatField(null=True, verbose_name='Saves Goals, Average %'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='saves_p_average_index',
            field=models.IntegerField(null=True, verbose_name='Saves Goals, Average % Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='saves_total',
            field=models.IntegerField(null=True, verbose_name='Saves Goals Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='saves_total_index',
            field=models.IntegerField(null=True, verbose_name='Saves Goals Total Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='sf_average',
            field=models.FloatField(null=True, verbose_name='Safety Factor Average'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='sf_average_index',
            field=models.FloatField(null=True, verbose_name='Safety Factor Average Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='shots_received_total',
            field=models.IntegerField(null=True, verbose_name='Shots Received Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='shots_received_total_index',
            field=models.IntegerField(null=True, verbose_name='Shots Received TOtal Index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='zero_goals_matches_total',
            field=models.IntegerField(null=True, verbose_name='0 Goals Matches'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='zero_goals_matches_total_index',
            field=models.IntegerField(null=True, verbose_name='0 Goals Matches Index'),
            preserve_default=True,
        ),
    ]
