# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_notecomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='pub_date',
            field=models.DateTimeField(editable=False, verbose_name='Дата публикации'),
        ),
    ]
