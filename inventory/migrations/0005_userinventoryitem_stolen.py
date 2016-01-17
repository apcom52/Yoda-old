# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20150929_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinventoryitem',
            name='stolen',
            field=models.BooleanField(verbose_name='Вещь уже продана', default=False),
        ),
    ]
