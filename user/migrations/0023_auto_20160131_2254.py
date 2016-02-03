# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_userprofile_lang'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='group',
            field=models.IntegerField(verbose_name='Подгруппа', choices=[(1, 'Первая подгруппа'), (2, 'Вторая подгруппа')], default=1),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='accent',
            field=models.CharField(verbose_name='Акцентный цвет', choices=[('red', 'Красный'), ('orange', 'Оранжевый'), ('yellow', 'Желтый'), ('olive', 'Оливковый'), ('green', 'Зеленый'), ('teal', 'Бирюзовый'), ('blue', 'Синий'), ('violet', 'Индиго'), ('purple', 'Фиолетовый'), ('pink', 'Пурпурный'), ('brown', 'Коричневый')], max_length=12, default='blue'),
        ),
    ]
