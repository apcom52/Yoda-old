# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0003_auto_20150808_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='login',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
