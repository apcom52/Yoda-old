# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryfile',
            name='description',
            field=models.TextField(null=True, blank=True, verbose_name='Описание файла'),
        ),
        migrations.AlterField(
            model_name='libraryfile',
            name='file',
            field=models.FileField(upload_to='uploads/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='libraryfile',
            name='pub_date',
            field=models.DateTimeField(null=True, blank=True, editable=False, verbose_name='Дата публикации'),
        ),
    ]
