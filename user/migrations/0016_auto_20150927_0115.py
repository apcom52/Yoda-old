# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_userprofile_bonus_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bonus_points',
            field=models.IntegerField(verbose_name='Бонусные очки', blank=True, default=0, null=True),
        ),
    ]
