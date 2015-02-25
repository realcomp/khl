# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_instagramimagefile_user_str'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instagramimagefile',
            options={'ordering': ('created', 'pk'), 'verbose_name': 'Instagram image file', 'verbose_name_plural': 'Instagram image files'},
        ),
    ]
