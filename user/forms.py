from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
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