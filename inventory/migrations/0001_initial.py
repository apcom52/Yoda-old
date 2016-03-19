# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Smile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='Название смайлика', max_length=64)),
                ('symbol', models.CharField(verbose_name='Обозначение смайлика', max_length=32)),
                ('icon', models.ImageField(verbose_name='Иконка смайлика', default='img/2015/08/04/ufo.jpg', upload_to='smiles/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='SmileCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='Название коллекции', max_length=128)),
                ('price_low', models.IntegerField(verbose_name='Цена за барахло')),
                ('price_med', models.IntegerField(verbose_name='Цена за качественную вещь')),
                ('price_high', models.IntegerField(verbose_name='Цена за дорогую вещь')),
                ('icon', models.ImageField(verbose_name='Иконка набора смайликов', default='img/2015/08/04/ufo.jpg', upload_to='smiles/%Y/%m/%d/')),
                ('smiles', models.ManyToManyField(to='inventory.Smile')),
            ],
        ),
    ]
