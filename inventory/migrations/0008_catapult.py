# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0007_itemcollection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catapult',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('view', models.BooleanField(default=False, verbose_name='Просмотрено')),
                ('from_user', models.ForeignKey(related_name='sender', null=True, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(to='inventory.UserInventoryItem')),
                ('to_user', models.ForeignKey(related_name='getter', null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
