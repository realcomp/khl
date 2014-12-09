# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('uin', models.CharField(unique=True, max_length=255, verbose_name=b'UIN \xd0\x9a\xd0\xbe\xd0\xbc\xd0\xbf\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb8')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f',
                'verbose_name_plural': '\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-id', '-date_joined'), 'verbose_name': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', 'verbose_name_plural': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438'},
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xbc\xd0\xbf\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f', blank=True, to='accounts.Company', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='fio',
            field=models.CharField(max_length=1024, verbose_name=b'\xd0\xa4\xd0\x98\xd0\x9e', blank=True),
        ),
    ]
