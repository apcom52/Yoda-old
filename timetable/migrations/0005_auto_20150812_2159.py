# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0004_notstudytime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notstudytime',
            old_name='end',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='notstudytime',
            old_name='start',
            new_name='start_date',
        ),
    ]
