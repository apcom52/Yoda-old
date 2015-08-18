# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0009_transferredlesson_lesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanceledLesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('last_date', models.DateField(verbose_name='Дата')),
                ('last_time', models.IntegerField(verbose_name='Номер пары', choices=[(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), (4, '4 пара'), (5, '5 пара'), (6, '6 пара'), (7, '7 пара')])),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
