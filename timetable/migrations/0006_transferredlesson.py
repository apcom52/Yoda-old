# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0005_auto_20150812_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferredLesson',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('last_date', models.DateField(verbose_name='Старая дата')),
                ('last_lesson', models.IntegerField(choices=[(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), (4, '4 пара'), (5, '5 пара'), (6, '6 пара'), (7, '7 пара')], verbose_name='Старый номер пары')),
                ('new_date', models.DateField(verbose_name='Новая дата')),
                ('new_lesson', models.IntegerField(choices=[(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), (4, '4 пара'), (5, '5 пара'), (6, '6 пара'), (7, '7 пара')], verbose_name='Новый номер пары')),
                ('new_place', models.IntegerField(verbose_name='Аудитория')),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
