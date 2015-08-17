# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=32, verbose_name='Пользователь')),
                ('text', models.CharField(max_length=1024, verbose_name='Сопроводительный текст')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='Дата')),
            ],
            options={
                'db_table': 'actions',
                'verbose_name_plural': 'Действия',
                'verbose_name': 'Действие',
            },
        ),
    ]
