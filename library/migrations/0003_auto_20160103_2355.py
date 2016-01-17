# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20160102_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarytag',
            name='views',
            field=models.IntegerField(verbose_name='Количество просмотров', default=0),
        ),
        migrations.AlterField(
            model_name='libraryfile',
            name='tags',
            field=models.ManyToManyField(null=True, to='library.LibraryTag', blank=True),
        ),
    ]
