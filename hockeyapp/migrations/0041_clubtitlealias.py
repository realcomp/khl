# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_titlealias'),
        ('hockeyapp', '0040_auto_20150204_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubTitleAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.OneToOneField(to='base.TitleAlias')),
                ('club', models.ForeignKey(to='hockeyapp.Club')),
            ],
            options={
                'verbose_name': 'Club title alias',
                'verbose_name_plural': 'Club title aliases ',
            },
            bases=(models.Model,),
        ),
    ]
