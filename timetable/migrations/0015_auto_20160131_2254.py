# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0014_auto_20150927_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='group',
            field=models.IntegerField(verbose_name='Подгруппа', choices=[(1, 'Первая подгруппа'), (2, 'Вторая подгруппа')], default=1),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='semester',
            field=models.IntegerField(verbose_name='Семестр', choices=[(1, 'Первый семестр'), (2, 'Второй семестр'), (3, 'Третий семестр'), (4, 'Четвертый семестр'), (5, 'Пятый семестр'), (6, 'Шестой семестр'), (7, 'Седьмой семестр'), (8, 'Восьмой семестр')], default=2),
        ),
    ]
