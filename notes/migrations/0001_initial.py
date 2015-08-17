# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('login', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'notes',
            },
        ),
    ]
