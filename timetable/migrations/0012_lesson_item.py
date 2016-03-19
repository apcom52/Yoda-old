# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0011_auto_20150819_0015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson_Item',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='Название предмета')),
            ],
        ),
    ]
