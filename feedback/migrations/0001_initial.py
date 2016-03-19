# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=128, verbose_name='Заголовок поста')),
                ('content', models.TextField(verbose_name='Содержимое поста')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата публикации')),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('content', models.CharField(max_length=256, verbose_name='Текст')),
                ('status', models.IntegerField(choices=[(0, 'Неизвестно'), (1, 'Выполнено'), (2, 'В процессе выполнения'), (3, 'Отклонено')], default=0, verbose_name='Статус')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата публикации')),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
