# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_auto_20160114_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='lang',
            field=models.CharField(choices=[('ru', 'Русский язык'), ('en', 'Английский язык')], max_length=2, default='ru', verbose_name='Язык интерфейса'),
        ),
    ]
