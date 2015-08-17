# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20150804_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to='img/%Y/%m/%d/', verbose_name='Фотография пользователя', default='img/2015/08/04/ufo.jpg'),
        ),
    ]
