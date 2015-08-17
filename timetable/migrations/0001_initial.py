# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField(verbose_name='Дата (YYYY-MM-DD)')),
                ('time', models.IntegerField(default=1, verbose_name='Номер пары', choices=[(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), (4, '4 пара'), (5, '5 пара'), (6, '6 пара'), (7, '7 пара')])),
                ('info', models.CharField(max_length=1024, verbose_name='Подробности')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField(verbose_name='Дата (YYYY-MM-DD)')),
                ('time', models.IntegerField(default=1, verbose_name='Номер пары', choices=[(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), (4, '4 пара'), (5, '5 пара'), (6, '6 пара'), (7, '7 пара')])),
                ('homework', models.CharField(max_length=1024, verbose_name='Домашнее задание')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='Название предмета')),
                ('semester', models.IntegerField(default=1, verbose_name='Семестр', choices=[(1, 'Первый семестр'), (2, 'Второй семестр'), (3, 'Третий семестр'), (4, 'Четвертый семестр'), (5, 'Пятый семестр'), (6, 'Шестой семестр'), (7, 'Седьмой семестр'), (8, 'Восьмой семестр')])),
                ('type', models.IntegerField(default=1, verbose_name='Тип занятия', choices=[(1, 'Лекция'), (2, 'Практика'), (3, 'Лабораторная работа')])),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='ФИО преподавателя')),
                ('semester', models.IntegerField(verbose_name='Семестр', choices=[(1, 'Первый семестр'), (2, 'Второй семестр'), (3, 'Третий семестр'), (4, 'Четвертый семестр'), (5, 'Пятый семестр'), (6, 'Шестой семестр'), (7, 'Седьмой семестр'), (8, 'Восьмой семестр')])),
                ('avatar', models.ImageField(upload_to='img/%Y/%m/%d/', default='img/2015/08/04/ufo.jpg', verbose_name='Фотография преподавателя')),
                ('lessons', models.ManyToManyField(to='timetable.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('semester', models.IntegerField(default=1, verbose_name='Семестр', choices=[(1, 'Первый семестр'), (2, 'Второй семестр'), (3, 'Третий семестр'), (4, 'Четвертый семестр'), (5, 'Пятый семестр'), (6, 'Шестой семестр'), (7, 'Седьмой семестр'), (8, 'Восьмой семестр')])),
                ('week', models.IntegerField(default=1, verbose_name='Неделя', choices=[(1, 'Нечетная неделя'), (2, 'Четная неделя')])),
                ('day', models.IntegerField(default=1, verbose_name='День', choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота')])),
                ('time', models.IntegerField(default=1, verbose_name='Номер пары', choices=[(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), (4, '4 пара'), (5, '5 пара'), (6, '6 пара'), (7, '7 пара')])),
                ('place', models.CharField(max_length=16, verbose_name='Аудитория')),
                ('double', models.BooleanField(default=False, verbose_name='Сдвоенная пара')),
                ('lesson', models.ForeignKey(to='timetable.Lesson')),
                ('teacher', models.ForeignKey(to='timetable.Teacher')),
            ],
        ),
    ]
