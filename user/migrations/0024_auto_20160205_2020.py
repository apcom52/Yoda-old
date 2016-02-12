# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_auto_20160131_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='events_notification',
            field=models.BooleanField(default=True, verbose_name='Высылать уведомления о ближайших событиях'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='events_time_notification',
            field=models.IntegerField(default=1, verbose_name='Уведомлять о событии', choices=[(1, 'За 1 день до начала'), (2, 'За 2 дня до начала'), (3, 'За 3 дня до начала')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='filter_achievements',
            field=models.BooleanField(default=True, verbose_name='Скрывать записи о достижениях'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='filter_bonuses',
            field=models.BooleanField(default=True, verbose_name='Скрывать записи о бонусах'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='filter_catapult',
            field=models.BooleanField(default=True, verbose_name='Скрывать записи о запусках катапульты'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='filter_sales',
            field=models.BooleanField(default=True, verbose_name='Скрывать записи о продажах'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='github',
            field=models.CharField(blank=True, max_length=256, verbose_name='Github', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='hide_tips',
            field=models.BooleanField(default=False, verbose_name='Скрывать подсказки'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notes_font_size',
            field=models.IntegerField(default=16, verbose_name='Размер шрифта в заметках', choices=[(14, '14px'), (16, '16px'), (18, '18px'), (20, '20px')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notes_font_style',
            field=models.IntegerField(default=1, verbose_name='Стиль шрифта в заметках', choices=[(1, 'Без засечек'), (2, 'С засечками')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notes_night_mode',
            field=models.BooleanField(default=False, verbose_name='Скрывать подсказки'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='polls_actual',
            field=models.BooleanField(default=True, verbose_name='Показывать актуальные темы'),
        ),
    ]
