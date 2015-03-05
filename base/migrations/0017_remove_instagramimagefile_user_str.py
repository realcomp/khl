# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20150226_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagramimagefile',
            name='user_str',
        ),
    ]
