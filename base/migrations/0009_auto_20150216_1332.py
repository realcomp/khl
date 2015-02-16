# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_instagramimagefile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramimagefile',
            name='data',
            field=picklefield.fields.PickledObjectField(editable=False),
            preserve_default=True,
        ),
    ]
