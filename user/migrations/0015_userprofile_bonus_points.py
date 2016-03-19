# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20150920_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bonus_points',
            field=models.IntegerField(null=True, blank=True, verbose_name='Бонусные очки'),
        ),
    ]
