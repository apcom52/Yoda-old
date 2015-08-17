# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='favorite_id',
            new_name='fav_id',
        ),
        migrations.RenameField(
            model_name='favorite',
            old_name='type',
            new_name='fav_type',
        ),
        migrations.AddField(
            model_name='favorite',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 5, 21, 27, 25, 745193, tzinfo=utc), verbose_name='Дата', auto_now=True),
            preserve_default=False,
        ),
    ]
