# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20141225_0907'),
        ('hockeyapp', '0011_match_league'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerCitizenship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='Start date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='End date', blank=True)),
                ('citizenship', models.ForeignKey(to='addresses.Country')),
                ('player', models.ForeignKey(to='hockeyapp.Player')),
            ],
            options={
                'verbose_name': 'Player citizenship',
                'verbose_name_plural': 'Players citizenships',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='player',
            name='contract_type',
            field=models.CharField(blank=True, max_length=32, verbose_name='Contract type', choices=[('', ''), (b'\xd0\x94\xd0\xb2\xd1\x83\xd1\x81\xd1\x82\xd0\xbe\xd1\x80\xd0\xbe\xd0\xbd\xd0\xbd\xd0\xb8\xd0\xb9 \xd0\x9a\xd0\xa5\xd0\x9b/\xd0\x9c\xd0\xa5\xd0\x9b', 'Two-sided KHL/MHL'), (b'\xd0\x94\xd0\xb2\xd1\x83\xd1\x81\xd1\x82\xd0\xbe\xd1\x80\xd0\xbe\xd0\xbd\xd0\xbd\xd0\xb8\xd0\xb9 \xd0\x9a\xd0\xa5\xd0\x9b/\xd0\x92\xd0\xa5\xd0\x9b', 'Two-sided KHL/VHL'), (b'\xd0\x9e\xd0\xb4\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd0\xbe\xd1\x80\xd0\xbe\xd0\xbd\xd0\xbd\xd0\xb8\xd0\xb9 \xd0\x9a\xd0\xa5\xd0\x9b', 'One-sided KHL')]),
            preserve_default=True,
        ),
    ]
