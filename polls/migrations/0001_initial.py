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
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('text', models.CharField(verbose_name='Ответ', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='PollComment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('comment', models.CharField(verbose_name='Комментарий', max_length=4096)),
                ('attaches', models.CharField(verbose_name='Прикрепления', default='', max_length=6144, blank=True, null=True)),
                ('answer_date', models.DateTimeField(editable=False, verbose_name='Дата публикации')),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QueAns',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('answer', models.IntegerField(default=0)),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='Вопрос', max_length=128)),
                ('type', models.IntegerField(verbose_name='Тип опроса', choices=[(1, 'Один вариант ответа'), (2, 'Несколько вариантов ответа')])),
                ('is_anon', models.BooleanField(verbose_name='Анонимность', default=False)),
                ('is_closed', models.BooleanField(verbose_name='Закрытый опрос')),
                ('pub_date', models.DateTimeField(editable=False, verbose_name='Дата публикации')),
                ('choices', models.ManyToManyField(to='polls.Answer')),
                ('login', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='queans',
            name='question',
            field=models.ForeignKey(to='polls.Question'),
        ),
        migrations.AddField(
            model_name='pollcomment',
            name='poll',
            field=models.ForeignKey(to='polls.Question'),
        ),
    ]
