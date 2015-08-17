# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_teachertimetable'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotStudyTime',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('start', models.DateField(verbose_name='От')),
                ('end', models.DateField(verbose_name='До')),
                ('info', models.CharField(blank=True, null=True, max_length=256, verbose_name='Подробности')),
            ],
        ),
    ]
