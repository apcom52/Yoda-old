from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings
from timetable.models import Lesson_Item
from inventory.models import Background
# Create your models here.

class Attendance(models.Model): #Посещаемость
	types = ((1, 'Лекция'),	(2, 'Практика'), (3, 'Лабораторная работа'))
	groups = ((0, 'Общее занятие'), (1, 'Первая подгруппа'), (2, 'Вторая подгруппа'))

	lesson = models.ForeignKey(Lesson_Item)
	date = models.DateField('Дата предмета')
	type = models.IntegerField('Тип занятия', choices = types, default = 1)
	group = models.IntegerField('Подгруппа', choices = groups, default = 0)
	visitor = models.ManyToManyField(User)

	class Meta:
		verbose_name = 'Посещаемость'
		verbose_name_plural = 'Посещаемость'

class AttendanceAdmin(admin.ModelAdmin):
	list_display = ('lesson', 'date', 'type')

	def get_form(self, request, obj=None, **kwargs):
		form = super(AttendanceAdmin, self).get_form(request, obj, **kwargs)
		form.base_fields['lesson'].queryset = Lesson_Item.objects.filter(semester = settings.SEMESTER)
		form.base_fields['visitor'].queryset = User.objects.filter(is_active = True)
		return form

class Duty(models.Model): #Долги
	groups = ((0, 'Общее занятие'), (1, 'Первая подгруппа'), (2, 'Вторая подгруппа'))

	lesson = models.ForeignKey(Lesson_Item)
	date = models.DateField('Дата предмета')
	description = models.CharField('Описание долга', max_length = 128, unique = False)
	group = models.IntegerField('Подгруппа', choices = groups, default = 0)
	visitors = models.ManyToManyField(User)

	class Meta:
		verbose_name = 'Долг'
		verbose_name_plural = 'Долги'

class DutyAdmin(admin.ModelAdmin):
	list_display = ('lesson', 'date', 'description')

	def get_form(self, request, obj=None, **kwargs):
		form = super(DutyAdmin, self).get_form(request, obj, **kwargs)
		form.base_fields['lesson'].queryset = Lesson_Item.objects.filter(semester = settings.SEMESTER)
		form.base_fields['visitor'].queryset = User.objects.filter(is_active = True)
		return form

class BonusPoints(models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField('Дата получения', auto_now = True)
	bonus = models.IntegerField('Кол-во очков')
	bingo = models.BooleanField('Случайный бонус', default = False)

class BonusPointsAdmin(admin.ModelAdmin):
	list_display = ('user', 'date', 'bonus', 'bingo')

class UserProfile(models.Model):
	themes = (('light', 'Светлая'),	('dark', 'Темная'))
	accents = (
		('red', 'Красный'),
		('orange', 'Оранжевый'),
		('yellow', 'Желтый'),
		('olive', 'Оливковый'),
		('green', 'Зеленый'),
		('teal', 'Бирюзовый'),
		('blue', 'Синий'),
		('violet', 'Индиго'),
		('purple', 'Фиолетовый'),
		('pink', 'Пурпурный'),
		('brown', 'Коричневый'),
		)
	languages = (
		('ru', 'Русский язык'),
		('en', 'Английский язык'),
		)
	groups = ((1, 'Первая подгруппа'), (2, 'Вторая подгруппа'))

	user = models.OneToOneField(User)
	group = models.IntegerField('Подгруппа', choices = groups, default = 1)
	last_visit = models.DateTimeField('Последний просмотр', blank = True, null = True)
	bonus_points = models.IntegerField('Бонусные очки', blank = True, null = True, default = 0)
	avatar = models.ImageField(upload_to='img/%Y/%m/%d/', verbose_name='Фотография пользователя', default='img/2015/08/04/ufo.jpg')
	facebook = models.CharField('Facebook', max_length = 256, blank = True, null = True)
	twitter = models.CharField('Twitter', max_length = 256, blank = True, null = True)
	vk = models.CharField('ВКонтакте', max_length = 256, blank = True, null = True)
	phone = models.CharField('Номер телефона', max_length = 16, blank = True, null = True)
	github = models.CharField('Github', max_length = 256, blank = True, null = True)
	
	theme = models.CharField('Тема', choices = themes, default = 'light', max_length = 8)
	accent = models.CharField('Акцентный цвет', choices = accents, default = 'blue', max_length = 12)
	lang = models.CharField('Язык интерфейса', choices = languages, default = 'ru', max_length=2)
	beta = models.BooleanField('Бета-функции', default = False)
	hide_email = models.BooleanField('Скрывать адрес e-mail', default = False)
	hide_tips = models.BooleanField('Скрывать подсказки', default = False)

	filter_achievements = models.BooleanField('Показывать записи о достижениях', default = True)
	filter_sales = models.BooleanField('Показывать записи о продажах', default = True)
	filter_catapult = models.BooleanField('Показывать записи о запусках катапульты', default = True)
	filter_bonuses = models.BooleanField('Показывать записи о бонусах', default = True)

	notes_font_sizes = (
		(14, '14px'),
		(16, '16px'),
		(18, '18px'),
		(20, '20px')
	)
	notes_font_styles = (
		(1, 'Без засечек'),
		(2, 'С засечками'),
	)

	notes_night_mode = models.BooleanField('Скрывать подсказки', default = False)
	notes_font_size = models.IntegerField('Размер шрифта в заметках', choices = notes_font_sizes, default = 16)
	notes_font_style = models.IntegerField('Стиль шрифта в заметках', choices = notes_font_styles,  default = 1)

	polls_actual = models.BooleanField('Показывать актуальные темы', default = True)

	events_time_notifications = (
		(1, 'За 1 день до начала'),
		(2, 'За 2 дня до начала'),
		(3, 'За 3 дня до начала'),
	)
	events_notification = models.BooleanField('Высылать уведомления о ближайших событиях', default = True)
	events_time_notification = models.IntegerField('Уведомлять о событии', choices = events_time_notifications, default = 1)

	class Meta:
		verbose_name = 'Профиль'
		verbose_name_plural = 'Профили'
