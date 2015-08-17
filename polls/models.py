from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class Answer(models.Model):
	text = models.CharField('Ответ', max_length = 64, unique = False)

	def __str__(self):
		return self.text


class Question(models.Model):
	types = ((1, 'Один вариант ответа'), (2, 'Несколько вариантов ответа'))

	login = models.ForeignKey(User)
	title = models.CharField('Вопрос', max_length = 128, unique = False)
	choices = models.ManyToManyField(Answer)
	type = models.IntegerField('Тип опроса', choices = types)
	is_anon = models.BooleanField('Анонимность', default = False)
	is_closed = models.BooleanField('Закрытый опрос')
	pub_date = models.DateTimeField('Дата публикации', editable = False)

	def __str__(self):
		return self.title

class QueAns(models.Model):
	login = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer = models.IntegerField(default = 0)

	def __str__(self):
		return "%s - %s (%s)" % (self.login.username, self.question.title, self.answer)

class PollComment(models.Model):
	login = models.ForeignKey(User)
	poll = models.ForeignKey(Question)
	comment = models.CharField('Комментарий', max_length = 4096)
	attaches = models.CharField('Прикрепления', max_length = 6144, default = '', blank = True, null = True)
	pub_date = models.DateTimeField('Дата публикации', editable = False)

class PollCommentAdmin(admin.ModelAdmin):
	list_display = ('login', 'poll', 'comment')