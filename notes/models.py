from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
	class Meta():
		db_table = 'notes'
		verbose_name = 'Заметка'
		verbose_name_plural = 'Заметки'

	title = models.CharField('Заголовок', max_length = 256)
	content = models.TextField('Содержание')
	pub_date = models.DateTimeField('Дата публикации', editable = False)
	login = models.ForeignKey(User)
	views = models.IntegerField(default = 0)

	def __str__(self):
		return self.title

class NoteAdmin(admin.ModelAdmin):
	fields = ('title', 'content', 'login')
	list_display = ('title', 'pub_date', 'login')

class NoteComment(models.Model):
	login = models.ForeignKey(User)
	note = models.ForeignKey(Note)
	comment = models.CharField('Комментарий', max_length = 4096)
	attaches = models.CharField('Прикрепления', max_length = 6144, default = '', blank = True, null = True)
	pub_date = models.DateTimeField('Дата публикации', editable = False)

class NoteCommentAdmin(admin.ModelAdmin):
	list_display = ('login', 'note', 'comment')