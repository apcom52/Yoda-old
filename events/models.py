from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
	title = models.CharField('Название мероприятия', max_length = 128)
	description = models.CharField('Описание мероприятия', max_length = 512, blank = True, null = True)
	date = models.DateTimeField('Дата и время проведения')
	is_required = models.BooleanField('Обязательное мероприятие', default = False)
	login = models.ForeignKey(User)

	def __str__(self):
		return self.title

class EventAdmin(admin.ModelAdmin):
	list_display = ('title', 'date', 'description', 'is_required')

class UserVisitEvent(models.Model):
	answers = ((1, 'Пойдет'), (2, 'Возможно пойдет'), (3, 'Не пойдет'))
	login = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	answer = models.IntegerField('Ответ', choices = answers)

	def __str__(self):
		return '%s -> %s (%s)' % (self.login, self.event, self.answers[self.answer])

class UserVisitEventAdmin(admin.ModelAdmin):
	list_display = ('login', 'event', 'answer')