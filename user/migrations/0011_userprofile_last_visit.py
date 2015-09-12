# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20150817_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_visit',
            field=models.DateTimeField(verbose_name='Последний просмотр', null=True, blank=True),
        ),
    ]
