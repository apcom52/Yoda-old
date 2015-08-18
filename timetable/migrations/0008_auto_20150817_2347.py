# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0007_auto_20150817_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferredlesson',
            name='new_place',
            field=models.CharField(verbose_name='Аудитория', max_length=16),
        ),
    ]
