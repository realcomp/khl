# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def parse_count(apps, schema_editor):
    Match = apps.get_model('hockeyapp', 'Match')
    for match in Match.objects.filter(count__isnull=False).none():
        if match.count:
            home_count, _, guest_count = match.count.partition(':')
            match.home_count = int(filter(
                lambda x: x.isdigit(), home_count) or 0)
            match.guest_count = int(filter(
                lambda x: x.isdigit(), guest_count) or 0)
            match.save()


class Migration(migrations.Migration):

    dependencies = [
        ('hockeyapp', '0084_auto_20150514_1905'),
    ]

    operations = [
        migrations.RunPython(parse_count, lambda x, y: None),
    ]
