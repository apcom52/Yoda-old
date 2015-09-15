# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0008_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_view',
            field=models.BooleanField(default=False, verbose_name='Просмотрено'),
        ),
    ]
