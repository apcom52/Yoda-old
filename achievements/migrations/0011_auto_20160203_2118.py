# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0010_action_important'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='author',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='is_anon',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='is_system',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='is_view',
        ),
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.IntegerField(choices=[(1, 'Обычное уведомление'), (2, 'Системное уведомление')], default=1, verbose_name='Тип уведомления'),
        ),
        migrations.AddField(
            model_name='notification',
            name='view',
            field=models.BooleanField(default=False, verbose_name='Уведомление просмотрено'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата и время получения'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='text',
            field=models.CharField(verbose_name='Текст уведомления', max_length=256),
        ),
        migrations.AlterField(
            model_name='notification',
            name='title',
            field=models.CharField(verbose_name='Заголовок уведомления', max_length=128),
        ),
    ]
