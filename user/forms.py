from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from achievements.models import Notification
from .models import UserProfile

class UploadAvatarForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ['avatar']

class ChangePasswordForm(forms.Form):
	password_old = forms.CharField(widget=forms.PasswordInput(), label="Текущий пароль:")
	password_new = forms.CharField(widget=forms.PasswordInput(), label="Новый пароль:")
	password_new2 = forms.CharField(widget=forms.PasswordInput(), label="Повторите новый пароль:")

class SetContactForm(forms.Form):
	vk = forms.CharField(label = 'ВКонтакте')
	facebook = forms.CharField(label = 'Facebook')
	twitter = forms.CharField(label = 'Twitter')
	phone = forms.CharField(label = 'Номер телефона')

class AddNotificationForm(forms.Form):
	users = (
		('apakin', 'Андрей Апакин'),
		('burkov', 'Андрей Бурков'),
		('zonov', 'Максим Зонов'),
		('kalashnikov', 'Сергей Калашников'),
		('kroshihina', 'Анастасия Крошихина'),
		('leyshin', 'Влад Леушин'),
		('apcom52', 'Александр Перевезенцев'),
		('selivanov', 'Михаил Селиванов'),
		('trofimenko', 'Влад Трофименко'),
		('tsekanov', 'Алексей Цеканов'),
		('sheromov', 'Константин Шеромов'),
		('shyklin', 'Вячеслав Шуклин'),
	)

	title = forms.CharField(label = 'Заголовок', max_length = 64)
	context = forms.CharField(label = 'Заголовок', max_length = 140)
	aims = forms.MultipleChoiceField(choices=users, label="Пользователи, которые получат уведомление (удерживайте CTRL для выделения нескольких человек)") 
	is_system = forms.BooleanField(label = 'Системное уведомление')
	is_anon = forms.BooleanField(label = 'Анонимное уведомление')