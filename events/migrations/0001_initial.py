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
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='Название мероприятия')),
                ('description', models.CharField(blank=True, null=True, max_length=512, verbose_name='Описание мероприятия')),
                ('date', models.DateTimeField(verbose_name='Дата и время проведения')),
                ('is_required', models.BooleanField(default=False, verbose_name='Обязательное мероприятие')),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserVisitEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('answer', models.IntegerField(choices=[(1, 'Пойдет'), (2, 'Возможно пойдет'), (3, 'Не пойдет')], verbose_name='Ответ')),
                ('event', models.ForeignKey(to='events.Event')),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
