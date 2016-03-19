# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_remove_userprofile_background'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='accent',
            field=models.CharField(choices=[('red', 'Красный'), ('orange', 'Оранжевый'), ('yellow', 'Желтый'), ('olive', 'Оливковый'), ('green', 'Зеленый'), ('teal', 'Бирюзовый'), ('blue', 'Синий'), ('violet', 'Пурпурный'), ('purple', 'Фиолетовый'), ('pink', 'Розовый'), ('brown', 'Коричневый')], default='blue', verbose_name='Акцентный цвет', max_length=12),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='theme',
            field=models.CharField(choices=[('light', 'Светлая'), ('dark', 'Темная')], default='light', verbose_name='Тема', max_length=8),
        ),
    ]
