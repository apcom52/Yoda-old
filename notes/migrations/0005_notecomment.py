# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0004_auto_20150809_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteComment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('comment', models.CharField(max_length=4096, verbose_name='Комментарий')),
                ('attaches', models.CharField(null=True, blank=True, default='', max_length=6144, verbose_name='Прикрепления')),
                ('pub_date', models.DateTimeField(verbose_name='Дата публикации', editable=False)),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('note', models.ForeignKey(to='notes.Note')),
            ],
        ),
    ]
