# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20150805_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='facebook',
            field=models.CharField(verbose_name='Facebook', max_length=256, default=datetime.datetime(2015, 8, 17, 12, 14, 10, 479553, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(verbose_name='Номер телефона', max_length=16, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitter',
            field=models.CharField(verbose_name='Twitter', max_length=256, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='vk',
            field=models.CharField(verbose_name='ВКонтакте', max_length=256, default=0),
            preserve_default=False,
        ),
    ]
