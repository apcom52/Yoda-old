# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20150917_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='beta',
            field=models.BooleanField(verbose_name='Бета-функции', default=False),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='visitor',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='duty',
            name='visitors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
