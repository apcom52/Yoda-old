# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0002_achievement_achunlocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='login',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
