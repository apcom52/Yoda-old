# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInventoryItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('type', models.IntegerField(choices=[(1, 'Обычный предмет'), (2, 'Фон профиля'), (3, 'Набор смайликов')], verbose_name='Тип предмета')),
                ('item_id', models.IntegerField(verbose_name='Идентификатор предмета')),
                ('quality', models.IntegerField(choices=[(1, 'Низкое качество'), (2, 'Хорошее качество'), (3, 'Эксклюзивная вещь')], verbose_name='Качество предмета')),
                ('get_date', models.DateTimeField(auto_now=True, verbose_name='Дата получения предмета')),
                ('price', models.IntegerField(verbose_name='Цена за предмет')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
