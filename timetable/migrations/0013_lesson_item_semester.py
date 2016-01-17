# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0012_lesson_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson_item',
            name='semester',
            field=models.IntegerField(choices=[(1, 'Первый семестр'), (2, 'Второй семестр'), (3, 'Третий семестр'), (4, 'Четвертый семестр'), (5, 'Пятый семестр'), (6, 'Шестой семестр'), (7, 'Седьмой семестр'), (8, 'Восьмой семестр')], default=1, verbose_name='Семестр'),
        ),
    ]
