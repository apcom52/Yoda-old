# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='content',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='note',
            name='login',
            field=models.CharField(max_length=32, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='note',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Заголовок'),
        ),
    ]
