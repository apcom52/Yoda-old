from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from notes.models import Note
from library.models import LibraryFile

# Create your models here.


class Favorite(models.Model):
	# Типы избранного
	# - Заметки
	types = (
		(1, 'Заметка'),
		(2, 'Файл'),
	)
	login = models.ForeignKey(User)
	type = models.IntegerField('Тип закладки', choices = types)
	note = models.ForeignKey(Note, blank = True, null = True)
	file = models.ForeignKey(LibraryFile, blank = True, null = True)
	pub_date = models.DateTimeField('Дата', auto_now = True)

	def __str__(self):
		favorite_name = ''
		if self.type == 1:
			favorite_name = self.note.title
		elif self.type == 2:
			favorite_name = self.file.title
		return '%s -> %s' % (self.login, favorite_name)

class FavoriteAdmin(admin.ModelAdmin):
	fields = ('login', 'type', 'note', 'file')
	list_display = ('login', 'type', 'note', 'file')