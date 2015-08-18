# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0010_canceledlesson'),
    ]

    operations = [
        migrations.RenameField(
            model_name='canceledlesson',
            old_name='last_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='canceledlesson',
            old_name='last_time',
            new_name='time',
        ),
    ]
