from django import forms
from django.conf import settings
from .utils import DTControl

class AddHomeworkForm(forms.Form):
	lesson_nums = (
		(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), 
		(4, '4 пара'), (5, '5 пара'), (6, '6 пара'), 
		(7, '7 пара'), 
	)
	date = forms.DateField(label = 'Дата (в формате YYYY-MM-DD (2015-04-16))', input_formats = ['%Y-%m-%d'])
	time = forms.ChoiceField(label = 'Пара', choices = lesson_nums)
	homework = forms.CharField(label = 'Домашнее задание', widget = forms.Textarea())

class AddControlForm(forms.Form):
	lesson_nums = (
		(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), 
		(4, '4 пара'), (5, '5 пара'), (6, '6 пара'), 
		(7, '7 пара'), 
	)
	date = forms.DateField(label = 'Дата (в формате YYYY-MM-DD (2015-04-16))', input_formats = ['%Y-%m-%d'])
	time = forms.ChoiceField(label = 'Пара', choices = lesson_nums)
	info = forms.CharField(label = 'Подробности', required = False, max_length = 1024)

class ChangePlaceForm(forms.Form):
	lesson_nums = (
		(1, '1 пара'), (2, '2 пара'), (3, '3 пара'), 
		(4, '4 пара'), (5, '5 пара'), (6, '6 пара'), 
		(7, '7 пара'), 
	)
	date = forms.DateField(label = 'Дата (в формате YYYY-MM-DD (2015-04-16))', input_formats = ['%Y-%m-%d'])
	time = forms.ChoiceField(label = 'Пара', choices = lesson_nums)
	new_place = forms.CharField(label = 'Новая аудитория', required = True, max_length = 32)