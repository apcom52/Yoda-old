# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_attendance_duty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='visitor',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='duty',
            name='visitors',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
