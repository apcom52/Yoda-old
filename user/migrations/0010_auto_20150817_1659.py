# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20150817_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='facebook',
            field=models.CharField(blank=True, verbose_name='Facebook', null=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, verbose_name='Номер телефона', null=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='twitter',
            field=models.CharField(blank=True, verbose_name='Twitter', null=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='vk',
            field=models.CharField(blank=True, verbose_name='ВКонтакте', null=True, max_length=256),
        ),
    ]
