from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth 
from timetable.utils import addAction, setAch
from user.models import UserProfile

# Create your views here.

class SignUpForm(forms.Form):
	users = (
		('zonov Максим Зонов', 'Максим Зонов'),
		('leyshin Влад Леушин', 'Влад Леушин'),
		('apcom52 Александр Перевезенцев', 'Александр Перевезенцев'),
		('selivanov Михаил Селиванов', 'Михаил Селиванов'),
		('smetanin Иван Сметанин', 'Иван Сметанин'),
		('trofimenko Влад Трофименко', 'Влад Трофименко'),
		('tsekanov Алексей Цеканов', 'Алексей Цеканов'),
		('shyklin Вячеслав Шуклин', 'Вячеслав Шуклин'),
	)
	username = forms.ChoiceField(widget=forms.Select, choices=users, label="Ваше имя:")
	mail = forms.EmailField(label="E-mail:", max_length = 128, error_messages = {'invalid': 'Введенный e-mail неправильный. Формат ввода: username@provider.domain'})
	password1 = forms.CharField(widget=forms.PasswordInput(), label="Пароль:")
	password2 = forms.CharField(widget=forms.PasswordInput(), label="Повторите пароль:")

	def clean(self):
		data = self.cleaned_data
		if "password1" in data and "password2" in data and data['password1'] != data['password2']:
			raise forms.ValidationError('Пароли не совпадают')


class SignInForm(forms.Form):
	users = (
		('zonov', 'Максим Зонов'),
		('leyshin', 'Влад Леушин'),
		('apcom52', 'Александр Перевезенцев'),
		('selivanov', 'Михаил Селиванов'),
		('smetanin', 'Иван Сметанин'),
		('trofimenko', 'Влад Трофименко'),
		('tsekanov', 'Алексей Цеканов'),
		('shyklin', 'Вячеслав Шуклин'),
	)
	username = forms.ChoiceField(widget=forms.Select, choices=users, label="Ваше имя:")
	password = forms.CharField(widget=forms.PasswordInput(), label="Пароль:")


def signup(request):
	error = [False, '']
	form = SignUpForm()
	if request.method == 'POST':
		form = SignUpForm(request.POST)		
		userdata = (request.POST['username']).split()
		username = userdata[0]
		first_name = userdata[1]
		last_name = userdata[2]
		mail = request.POST['mail']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		if form.is_valid() and password1 == password2 and len(password1) >= 6:
			user = User.objects.create_user(username, mail, password1)
			user.first_name = first_name
			user.last_name = last_name
			user.is_active = True
			user.save()	
			userprofile = UserProfile()
			userprofile.user = user
			userprofile.vk = ''
			userprofile.facebook = ''
			userprofile.twitter = ''
			userprofile.phone = ''
			userprofile.save()
			# Добавление действия в ленту
			addAction(user, 'присоединился к сервису')	
			setAch(user, 1)
			return redirect('/auth/in')
		else:
			print('form not valid!')
			error[0] = True
			error[1] = 'Введенные данные содержат ошибку'	
	context = {"form": form, 'title': 'Регистрация', 'error': error[0], 'error_text': error[1]}
	return render(request, 'sign-up.html', context)

@csrf_exempt
def signin(request):
	users = []
	users_list = User.objects.all().filter(is_active = True)
	for user in users_list:
		users.append({
			'first_name': user.first_name,
			'avatar': user.userprofile.avatar.url,
			'username': user.username,
			'user': user,
		})
	if request.user.is_authenticated():
		olduser = request.user
	elif request.POST.get('username'):
		for user in users:
			if user['username'] == request.POST['username']:
				olduser = user
	else:
		import random
		olduser = random.choice(users)
	error = [False, '']
	form = SignInForm()
	if request.method == 'POST':
		form = SignInForm(request.POST)		
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username = username, password = password)
			if user is not None and user.is_active:
				if user.is_active:
					auth.login(request, user)
					return redirect('/')
				else:
					error[0], error[1] = True, 'Пользователь не найден или он не активен'
			else:
				error[0], error[1] = True, 'Введенные данные некорректны'
	context = {
		"form": form,
		'users': users, 
		'olduser': olduser,
		'error': error[0], 
		'error_text': error[1]
		}
	return render(request, 'beta/beta_sign-in.html', context)

def signout(request):
	logout(request)
	return redirect('/auth/in/')

def premier(request):
	return render(request, 'premier.html', {})

def game(request):
	return render(request, 'game.html', {})