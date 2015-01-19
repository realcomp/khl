# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools

from django.db import models, migrations


def split_fio(apps, schema_editor):
    Player = apps.get_model('hockeyapp', 'Player')
    Coach = apps.get_model('hockeyapp', 'Coach')
    Judge = apps.get_model('hockeyapp', 'Judge')
    for man in itertools.chain(
            *(Player.objects.all(), Coach.objects.all(),
              Judge.objects.all())):
        if man.ru_fio:
            man.ru_name, sep, man.ru_lastname = man.ru_fio.partition(' ')
        if man.en_fio:
            man.en_name, sep, man.en_lastname = man.en_fio.partition(' ')
        man.save()


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0031_auto_20150119_1418'),
    ]

    operations = [
        migrations.RunPython(split_fio),
    ]
