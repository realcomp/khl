# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
        ('hockeyapp', '0002_auto_20141221_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogoClubHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='Start date')),
                ('end_date', models.DateField(null=True, verbose_name='End date')),
                ('club', models.ForeignKey(to='hockeyapp.Club')),
                ('logo', filer.fields.image.FilerImageField(verbose_name='Logo', to='filer.Image')),
            ],
            options={
                'verbose_name': 'Logo Club History',
                'verbose_name_plural': 'Logo Club Histories',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='club',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='addresses.Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='arena',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Arena', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Coach', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='farm_club',
            field=models.OneToOneField(related_name='farmclubparent', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Club'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='junior_club',
            field=models.OneToOneField(related_name='juniorclubparent', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Club'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='logo',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Logo', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='guest_coach',
            field=models.ForeignKey(related_name='guestmatches', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Coach', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='guest_team',
            field=models.ForeignKey(related_name='guestmatches', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Guest team', blank=True, to='hockeyapp.Club', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='home_coach',
            field=models.ForeignKey(related_name='homematches', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hockeyapp.Coach', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='home_team',
            field=models.ForeignKey(related_name='homematches', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Home team', blank=True, to='hockeyapp.Club', null=True),
            preserve_default=True,
        ),
    ]
