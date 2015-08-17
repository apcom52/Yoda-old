# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'wall_post'), (2, 'note'), (3, 'event')], verbose_name='Тип закладки')),
                ('favorite_id', models.IntegerField(verbose_name='Идентификатор избранного')),
                ('login', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
