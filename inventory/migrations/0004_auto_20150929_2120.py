# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_background'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='Название фона', max_length=128)),
                ('image', models.ImageField(verbose_name='Фон', upload_to='background/%Y/%m/%d/', default='img/2015/08/04/ufo.jpg')),
                ('price_low', models.IntegerField(verbose_name='Цена за барахло')),
                ('price_med', models.IntegerField(verbose_name='Цена за качественную вещь')),
                ('price_high', models.IntegerField(verbose_name='Цена за дорогую вещь')),
            ],
        ),
        migrations.AddField(
            model_name='background',
            name='price_high',
            field=models.IntegerField(verbose_name='Цена за дорогую вещь', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='background',
            name='price_low',
            field=models.IntegerField(verbose_name='Цена за барахло', default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='background',
            name='price_med',
            field=models.IntegerField(verbose_name='Цена за качественную вещь', default=10),
            preserve_default=False,
        ),
    ]
