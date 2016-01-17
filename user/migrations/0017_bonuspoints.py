# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0016_auto_20150927_0115'),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusPoints',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата получения', auto_now=True)),
                ('bonus', models.IntegerField(verbose_name='Кол-во очков')),
                ('bingo', models.BooleanField(default=False, verbose_name='Случайный бонус')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
