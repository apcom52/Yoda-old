# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0006_auto_20150813_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('start_points', models.IntegerField(verbose_name='Начальное значение')),
                ('end_points', models.IntegerField(verbose_name='Конечное значение')),
                ('rank', models.CharField(verbose_name='Звание', max_length=32)),
            ],
        ),
    ]
