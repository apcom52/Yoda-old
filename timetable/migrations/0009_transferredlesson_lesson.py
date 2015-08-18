# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0008_auto_20150817_2347'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferredlesson',
            name='lesson',
            field=models.ForeignKey(default=0, to='timetable.Timetable'),
            preserve_default=False,
        ),
    ]
