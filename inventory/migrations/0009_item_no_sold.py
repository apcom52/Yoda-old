# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_catapult'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='no_sold',
            field=models.BooleanField(default=False, verbose_name='Не для продажи'),
        ),
    ]
