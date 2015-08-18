# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0006_transferredlesson'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transferredlesson',
            old_name='last_lesson',
            new_name='last_time',
        ),
        migrations.RenameField(
            model_name='transferredlesson',
            old_name='new_lesson',
            new_name='new_time',
        ),
    ]
