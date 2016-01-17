# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_userinventoryitem_stolen'),
    ]

    operations = [
        migrations.RenameField(
            model_name='background',
            old_name='image',
            new_name='icon',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='image',
            new_name='icon',
        ),
    ]
