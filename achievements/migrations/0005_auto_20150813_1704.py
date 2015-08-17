# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0004_auto_20150808_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='achunlocked',
            name='is_new',
            field=models.BooleanField(default=True, verbose_name='Просмотр'),
        ),
        migrations.AlterField(
            model_name='achunlocked',
            name='ach_id',
            field=models.ForeignKey(to='achievements.Achievement'),
        ),
        migrations.AlterField(
            model_name='achunlocked',
            name='login',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
