# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('achievements', '0007_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('author', models.IntegerField(verbose_name='ID отправителя')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='Дата отправления')),
                ('title', models.CharField(max_length=64, verbose_name='Заголовок')),
                ('text', models.CharField(max_length=140, verbose_name='Содержимое уведомления')),
                ('is_system', models.BooleanField(default=False, verbose_name='Системное уведомление')),
                ('is_anon', models.BooleanField(default=False, verbose_name='Анонимное уведомление')),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
