from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class Action(models.Model):
	class Meta():
		db_table = 'actions'
		verbose_name = 'Действие'
		verbose_name_plural = 'Действия'

	login = models.ForeignKey(User)
	text = models.CharField('Сопроводительный текст', max_length = 1024)
	pub_date = models.DateTimeField('Дата', auto_now = True)
	
	def __str__(self):
		return self.login.username + ' ' + self.text

class ActionAdmin(admin.ModelAdmin):
	list_display = ('login', 'text', 'pub_date')

class Achievement(models.Model):
	title = models.CharField('Название', max_length = 32)
	description = models.CharField('Описание', max_length = 64)
	xp = models.IntegerField('Опыт')
	icon = models.CharField('Ссылка на иконку', max_length = 128, blank = True, null = True)

	def __str__(self):
		return self.title

class AchievementAdmin(admin.ModelAdmin):
	fields = ('title', 'description', 'xp', 'icon')
	list_display = ('title', 'description', 'xp')

class AchUnlocked(models.Model):
	ach_id = models.ForeignKey(Achievement)
	login = models.ForeignKey(User)
	pub_date = models.DateTimeField('Дата', auto_now = True)
	is_new = models.BooleanField('Просмотр', default = True)

class AchUnlockedAdmin(admin.ModelAdmin):
	fields = ('ach_id', 'login')
	list_display = ('ach_id', 'login', 'pub_date')

class Rank(models.Model):
	start_points = models.IntegerField('Начальное значение')
	end_points = models.IntegerField('Конечное значение')
	rank = models.CharField('Звание', max_length = 32)

	def __str__(self):
		return self.rank

class RankAdmin(admin.ModelAdmin):
	list_display = ('rank', 'start_points', 'end_points')