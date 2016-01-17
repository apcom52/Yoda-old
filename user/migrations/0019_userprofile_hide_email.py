# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_userprofile_background'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='hide_email',
            field=models.BooleanField(default=False, verbose_name='Скрывать адрес e-mail'),
        ),
    ]
