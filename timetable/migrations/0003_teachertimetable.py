# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_newplace'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherTimetable',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('lesson', models.CharField(max_length=128, verbose_name='Предмет')),
                ('group', models.CharField(max_length=10, verbose_name='Группа')),
                ('semester', models.IntegerField(default=1, choices=[(1, 'Первый семестр'), (2, 'Второй семестр'), (3, 'Третий семестр'), (4, 'Четвертый семестр'), (5, 'Пятый семестр'), (6, 'Шестой семестр'), (7, 'Седьмой семестр'), (8, 'Восьмой семестр')], verbose_name='Семестр')),
                ('week', models.IntegerField(default=1, choices=[(1, 'Нечетная неделя'), (2, 'Четная неделя')], verbose_name='Неделя')),
                ('day', models.IntegerField(default=1, choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота')], verbose_name='День')),
                ('time', models.IntegerField(default=1, choices=[(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), (4, '4 пара'), (5, '5 пара'), (6, '6 пара'), (7, '7 пара')], verbose_name='Номер пары')),
                ('type', models.IntegerField(default=1, choices=[(1, 'Лекция'), (2, 'Практика'), (3, 'Лабораторная работа')], verbose_name='Тип занятия')),
                ('place', models.CharField(max_length=16, verbose_name='Аудитория')),
                ('double', models.BooleanField(default=False, verbose_name='Сдвоенная пара')),
                ('teacher', models.ForeignKey(to='timetable.Teacher')),
            ],
        ),
    ]
