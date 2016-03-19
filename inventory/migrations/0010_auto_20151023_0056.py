# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0009_item_no_sold'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Название раздачи')),
                ('view', models.BooleanField(default=False, verbose_name='Получено')),
            ],
        ),
        migrations.AlterField(
            model_name='userinventoryitem',
            name='quality',
            field=models.IntegerField(choices=[(1, 'Низкое качество'), (2, 'Хорошее качество'), (3, 'Эксклюзивная вещь'), (4, 'Легендарное качество')], verbose_name='Качество предмета'),
        ),
        migrations.AddField(
            model_name='distribution',
            name='items',
            field=models.ManyToManyField(to='inventory.UserInventoryItem'),
        ),
        migrations.AddField(
            model_name='distribution',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
