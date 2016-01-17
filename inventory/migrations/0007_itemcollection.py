# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20150929_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='Название коллекции', max_length=64)),
                ('items', models.ManyToManyField(to='inventory.Item')),
            ],
        ),
    ]
