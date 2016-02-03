# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20160103_2355'),
        ('notes', '0006_auto_20150815_1722'),
        ('favorites', '0002_auto_20150806_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='fav_id',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='fav_type',
        ),
        migrations.AddField(
            model_name='favorite',
            name='file',
            field=models.ForeignKey(null=True, to='library.LibraryFile', blank=True),
        ),
        migrations.AddField(
            model_name='favorite',
            name='note',
            field=models.ForeignKey(null=True, to='notes.Note', blank=True),
        ),
        migrations.AddField(
            model_name='favorite',
            name='type',
            field=models.IntegerField(default=1, choices=[(1, 'Заметка'), (2, 'Файл')], verbose_name='Тип закладки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='favorite',
            name='login',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
