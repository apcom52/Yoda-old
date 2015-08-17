# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0005_auto_20150813_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='icon',
            field=models.CharField(verbose_name='Ссылка на иконку', blank=True, max_length=128, null=True),
        ),
    ]
