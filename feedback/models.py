from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
	login = models.ForeignKey(User)
	title = models.CharField('Заголовок поста', max_length = 128)
	content = models.TextField('Содержимое поста')
	date = models.DateTimeField('Дата публикации', auto_now = True)

class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'date')

class Feedback(models.Model):
	statuses = (
		(0, 'Неизвестно'),
		(1, 'Выполнено'),
		(2, 'В процессе выполнения'),
		(3, 'Отклонено'),
	)
	login = models.ForeignKey(User)
	content = models.CharField('Текст', max_length = 256)
	status = models.IntegerField('Статус', choices = statuses, default = 0)
	date = models.DateTimeField('Дата публикации', auto_now = True)

class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('login', 'content', 'status')