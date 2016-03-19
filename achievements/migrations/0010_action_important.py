# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0009_notification_is_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='important',
            field=models.BooleanField(verbose_name='Важное сообщение', default=True),
        ),
    ]
