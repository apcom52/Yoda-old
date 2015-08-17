# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('achievements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Название')),
                ('description', models.CharField(max_length=64, verbose_name='Описание')),
                ('xp', models.IntegerField(verbose_name='Опыт')),
                ('icon', models.CharField(max_length=128, verbose_name='Ссылка на иконку')),
            ],
        ),
        migrations.CreateModel(
            name='AchUnlocked',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='Дата')),
                ('ach_id', models.OneToOneField(to='achievements.Achievement')),
                ('login', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
