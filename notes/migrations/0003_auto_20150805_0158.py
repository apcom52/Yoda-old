# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_auto_20150805_0118'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'verbose_name': 'Заметка', 'verbose_name_plural': 'Заметки'},
        ),
        migrations.AddField(
            model_name='note',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
