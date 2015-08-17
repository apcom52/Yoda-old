# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewPlace',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата (YYYY-MM-DD)')),
                ('time', models.IntegerField(verbose_name='Номер пары', default=1, choices=[(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), (4, '4 пара'), (5, '5 пара'), (6, '6 пара'), (7, '7 пара')])),
                ('new_place', models.CharField(max_length=1024, verbose_name='Подробности')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
