from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.


class Favorite(models.Model):
	# Типы избранного
	# - Записи на стене
	# - Заметки
	# - Мероприятия
	types = (
		(1, 'wall_post'),
		(2, 'note'),
		(3, 'event'),
	)
	login = models.OneToOneField(User)
	fav_type = models.IntegerField('Тип закладки', choices = types)
	fav_id = models.IntegerField('Идентификатор избранного')
	pub_date = models.DateTimeField('Дата', auto_now = True)

class FavoriteAdmin(admin.ModelAdmin):
	fields = ('login', 'fav_type', 'fav_id')
	list_display = ('login', 'fav_type', 'fav_id')