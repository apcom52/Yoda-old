# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0015_auto_20160131_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='group',
            field=models.IntegerField(choices=[(1, 'Общая пара'), (2, 'Первая подгруппа'), (3, 'Вторая подгруппа')], default=0, verbose_name='Подгруппа'),
        ),
    ]
