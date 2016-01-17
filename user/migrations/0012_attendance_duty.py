# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0012_lesson_item'),
        ('user', '0011_userprofile_last_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField(verbose_name='Дата предмета')),
                ('type', models.IntegerField(choices=[(1, 'Лекция'), (2, 'Практика'), (3, 'Лабораторная работа')], verbose_name='Тип занятия', default=1)),
                ('lesson', models.ForeignKey(to='timetable.Lesson_Item')),
                ('visitor', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField(verbose_name='Дата предмета')),
                ('description', models.CharField(max_length=128, verbose_name='Описание долга')),
                ('lesson', models.ForeignKey(to='timetable.Lesson_Item')),
                ('visitors', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
