# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_userprofile_hide_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='background',
        ),
    ]
