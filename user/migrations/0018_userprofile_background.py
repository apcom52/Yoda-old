# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_background'),
        ('user', '0017_bonuspoints'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='background',
            field=models.ForeignKey(to='inventory.Background', default=1),
            preserve_default=False,
        ),
    ]
