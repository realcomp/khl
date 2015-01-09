# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0013_auto_20150107_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='advancedplayerstats',
            name='fiver',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Fiver', choices=[(0, 'unknown'), (1, 1), (2, 2), (3, 3), (4, 4)]),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='block_1th',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='block_2nd',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='block_3th',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='block_all',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='change_count_1th',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='change_count_2nd',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='change_count_3th',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='change_count_all',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='foul_1th',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='foul_2nd',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='foul_3th',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='foul_all',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='gamingtime_1th',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='gamingtime_2nd',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='gamingtime_3th',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='gamingtime_all',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='hit_1th',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='hit_2nd',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='hit_3th',
        ),
        migrations.RemoveField(
            model_name='advancedplayerstats',
            name='hit_all',
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='block_1th',
            field=models.PositiveIntegerField(null=True, verbose_name='1th period blocks'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='block_2nd',
            field=models.PositiveIntegerField(null=True, verbose_name='2nd period blocks'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='block_3th',
            field=models.PositiveIntegerField(null=True, verbose_name='3th period blocks'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='block_all',
            field=models.PositiveIntegerField(null=True, verbose_name='All periods blocks'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='change_count_1th',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='1th period change count'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='change_count_2nd',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='2nd period change count'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='change_count_3th',
            field=models.PositiveIntegerField(null=True, verbose_name='3th period change count'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='change_count_all',
            field=models.PositiveIntegerField(null=True, verbose_name='All periods change count'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='foul_1th',
            field=models.PositiveIntegerField(null=True, verbose_name='1th period fouls'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='foul_2nd',
            field=models.PositiveIntegerField(null=True, verbose_name='2nd period fouls'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='foul_3th',
            field=models.PositiveIntegerField(null=True, verbose_name='3th period fouls'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='foul_all',
            field=models.PositiveIntegerField(null=True, verbose_name='All periods fouls'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='gamingtime_1th',
            field=models.PositiveIntegerField(null=True, verbose_name='1th period time in game'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='gamingtime_2nd',
            field=models.PositiveIntegerField(null=True, verbose_name='2nd period change count'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='gamingtime_3th',
            field=models.PositiveIntegerField(null=True, verbose_name='3th period time in game'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='gamingtime_all',
            field=models.PositiveIntegerField(null=True, verbose_name='All periods time in game'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='hit_1th',
            field=models.PositiveIntegerField(null=True, verbose_name='1th period hits'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='hit_2nd',
            field=models.PositiveIntegerField(null=True, verbose_name='2nd period hits'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='hit_3th',
            field=models.PositiveIntegerField(null=True, verbose_name='3th period hits'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedplayerstats',
            name='hit_all',
            field=models.PositiveIntegerField(null=True, verbose_name='All periods hits'),
            preserve_default=True,
        ),
    ]
