# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_userinventoryitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Background',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='Название фона')),
                ('image', models.ImageField(upload_to='background/%Y/%m/%d/', default='img/2015/08/04/ufo.jpg', verbose_name='Фон')),
            ],
        ),
    ]
