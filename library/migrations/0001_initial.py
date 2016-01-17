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
            name='LibraryFile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='Название файла')),
                ('description', models.TextField(verbose_name='Описание файла')),
                ('file', models.FileField(upload_to='/media/uploads/%Y/%m/%d')),
                ('pub_date', models.DateTimeField(verbose_name='Дата публикации', editable=False)),
                ('views', models.IntegerField(verbose_name='Количество просмотров', default=0)),
                ('downloads', models.IntegerField(verbose_name='Количество загрузок', default=0)),
                ('is_available', models.BooleanField(verbose_name='Файл доступен для загрузки', default=True)),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Файлы библиотеки',
                'verbose_name': 'Файл библиотеки',
            },
        ),
        migrations.CreateModel(
            name='LibraryTag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=64, verbose_name='Название тега')),
            ],
            options={
                'verbose_name_plural': 'Теги библиотеки',
                'verbose_name': 'Тег библиотеки',
            },
        ),
        migrations.CreateModel(
            name='LibraryTagCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='Название категории тега')),
                ('color', models.CharField(max_length=16, verbose_name='Цвет категории')),
            ],
            options={
                'verbose_name_plural': 'Категории тегов',
                'verbose_name': 'Категория тегов',
            },
        ),
        migrations.AddField(
            model_name='librarytag',
            name='tag_category',
            field=models.ForeignKey(to='library.LibraryTagCategory'),
        ),
        migrations.AddField(
            model_name='libraryfile',
            name='tags',
            field=models.ManyToManyField(to='library.LibraryTag'),
        ),
    ]
