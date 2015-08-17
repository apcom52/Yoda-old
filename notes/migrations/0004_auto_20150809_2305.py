# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20150805_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='login',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
