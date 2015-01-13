# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0017_match_spectators'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='bullet_goals',
            new_name='bullet_goals_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='es_goals',
            new_name='es_goals_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='ev_goals',
            new_name='ev_goals_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='faceoff',
            new_name='faceoff_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='gamingtime',
            new_name='gamingtime_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='loose_goals',
            new_name='loose_goals_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='overtime_goals',
            new_name='overtime_goals_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='penalty_time',
            new_name='penalty_time_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='pis',
            new_name='pis_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='plus_minus',
            new_name='plus_minus_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='pp_goals',
            new_name='pp_goals_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='saves_p',
            new_name='saves_p_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='saves',
            new_name='saves_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='sf',
            new_name='sf_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='shots',
            new_name='shots_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='win_goals',
            new_name='win_goals_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='winfaceoff_p',
            new_name='winfaceoff_p_str',
        ),
        migrations.RenameField(
            model_name='clubplayermatch',
            old_name='winfaceoff',
            new_name='winfaceoff_str',
        ),
    ]
