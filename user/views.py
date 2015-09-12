from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.forms import PasswordChangeForm
from timetable.utils import avatar, pointsumm, getrank, handle_uploaded_file
from achievements.models import Action, Achievement, AchUnlocked
from timetable.utils import addAction, setAch, checkAchievements, isOnline, UpdateStatus
from notes.models import Note
from polls.models import Question
from events.models import Event
from .forms import *
from .utils import getProfileInfo
import pymorphy2
import datetime

# Create your views here.
def profile(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		UpdateStatus(request.user)
		checkAchievements(request.user)		
		up = getProfileInfo(id)	

		context = {
			'title': up['title'],
			'user': up['user'],
			'bodyclass': 'profile-page',
			'avatar': up['avatar'],
			'friends': up['friends'],
			'actions': up['actions'],
			'active_page': 1,
			'actions_morph': up['actions_morph'],
			'xp': up['xp'],
			'xp_morph': up['xp_morph'],
			'ach_counter': up['ach_counter'],
			'ach_counter_morph': up['ach_counter_morph'],
			'last_achievements': up['last_achievements'],
			'rank': up['rank'],
			'contacts': up['contacts'],
			'phone': up['phone'],
			'is_online': up['is_online'],
			'last_visit': up['last_visit'],
		}
		return render(request, 'profile.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def achievements(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		UpdateStatus(request.user)
		checkAchievements(request.user)	
		up = getProfileInfo(id)	

		try:
			my_ach_list = AchUnlocked.objects.all().filter(login = up['user']).order_by('-pub_date')
			my_ach = []
			for ach in my_ach_list:
				my_ach.append({
					'title': ach.ach_id.title,
					'description': ach.ach_id.description,
					'xp': ach.ach_id.xp,
					'icon': ach.ach_id.icon,
				})
			exclude_names = [o.ach_id.title for o in my_ach_list] 
		except ObjectDoesNotExist:
			my_ach = []

		if my_ach: 
			not_my_ach_list = Achievement.objects.all().exclude(title__in = exclude_names)
		else:
			not_my_ach_list = Achievement.objects.all()
		achs = []
		for ach in not_my_ach_list:
			achs.append({
				'title': ach.title,
				'description': ach.description,
				'xp': ach.xp,
				'icon': ach.icon,
			})

		context = {
			'title': up['title'],
			'user': up['user'],
			'bodyclass': 'profile-page',
			'avatar': up['avatar'],
			'friends': up['friends'],
			'actions': up['actions'],
			'active_page': 2,
			'actions_morph': up['actions_morph'],
			'xp': up['xp'],
			'xp_morph': up['xp_morph'],
			'ach_counter': up['ach_counter'],
			'ach_counter_morph': up['ach_counter_morph'],
			'last_achievements': up['last_achievements'],
			'rank': up['rank'],
			'contacts': up['contacts'],
			'phone': up['phone'],
			'is_online': up['is_online'],
			'last_visit': up['last_visit'],
			'my_ach': my_ach,
			'achs': achs,
		}
		return render(request, 'profile-achievements.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def user_content(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		UpdateStatus(request.user)
		up = getProfileInfo(id)	

		try:
			my_notes_list = Note.objects.all().filter(login = up['user']).order_by('-pub_date')
			my_notes = []
			for note in my_notes_list:
				my_notes.append({
					'title': note.title,
					'id': note.id,
					'views': note.views,
				})
		except ObjectDoesNotExist:
			my_notes = []

		try:
			my_polls_list = Question.objects.all().filter(login = up['user']).order_by('-pub_date')
			my_polls = []
			for poll in my_polls_list:
				my_polls.append({
					'title': poll.title,
					'id': poll.id,
				})
		except ObjectDoesNotExist:
			my_polls = []

		now = datetime.datetime.now()
		try:
			my_events_list = Event.objects.all().filter(login = up['user'])
			my_events = []
			for event in my_events_list:
				date = datetime.datetime(event.date.year, event.date.month, event.date.day, event.date.hour, event.date.minute)
				date += datetime.timedelta(hours = 3)
				if now > date: is_ended = True
				else: is_ended = False
				my_events.append({
					'title': event.title,
					'id': event.id,
					'is_ended': is_ended,
				})
		except ObjectDoesNotExist:
			my_events = []

		context = {
			'title': up['title'],
			'user': up['user'],
			'bodyclass': 'profile-page',
			'avatar': up['avatar'],
			'friends': up['friends'],
			'actions': up['actions'],
			'active_page': 3,
			'actions_morph': up['actions_morph'],
			'xp': up['xp'],
			'xp_morph': up['xp_morph'],
			'ach_counter': up['ach_counter'],
			'ach_counter_morph': up['ach_counter_morph'],
			'last_achievements': up['last_achievements'],
			'rank': up['rank'],
			'contacts': up['contacts'],
			'phone': up['phone'],
			'is_online': up['is_online'],
			'last_visit': up['last_visit'],
			'notes': my_notes,
			'events': my_events,
			'polls': my_polls,
		}
		return render(request, 'profile_content.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def settings(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	UpdateStatus(request.user)
	avatar_upload = UploadAvatarForm()
	change_password = ChangePasswordForm()
	set_contacts = SetContactForm(initial = {'vk': request.user.userprofile.vk, 'facebook': request.user.userprofile.facebook, 'twitter': request.user.userprofile.twitter, 'phone': request.user.userprofile.phone})
	error_password = request.GET.get('error_password', False)
	context = {
		'title': 'Настройки',
		'current_avatar': avatar(request.user),
		'avatar_upload': avatar_upload,
		'change_password': change_password,
		'set_contacts': set_contacts,
		'error_password': error_password,
	}
	return render(request, 'settings.html', context)

def upload_photo(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if request.method == 'POST':
		form = UploadAvatarForm(request.POST, request.FILES)		

		if form.is_valid():
			try:
				newavatar = form.save(commit = False)
				me = UserProfile.objects.get(user = request.user)
				me.avatar = request.FILES['avatar']
				me.save()
				addAction(request.user, 'изменил свою фотографию<br><img src="%s" class="ui small image">' % (avatar(request.user)))
				setAch(request.user, 4)
			except MultiValueDictKeyError:
				pass
	return redirect('/users/settings/')

def set_contacts(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if request.method == 'POST':
		form = SetContactForm(request.POST)
		data = request.POST
		vk = data.get('vk', False)
		facebook = data.get('facebook', False)
		twitter = data.get('twitter', False)
		phone = data.get('phone', False)

		#Форматируем введенные данные
		for c in (vk, facebook, twitter):
			c.strip()
			c.replace('http://', '')
			c.replace('https://', '')
			c.replace('www.', '')
		vk.replace('vk.com/', '')
		facebook.replace('facebook.com/', '')
		twitter.replace('twitter.com/', '')

		mycontacts = UserProfile.objects.get(user = request.user)
		mycontacts.vk = data['vk']
		mycontacts.facebook = data['facebook']
		mycontacts.twitter = data['twitter']
		mycontacts.phone = data['phone']
		mycontacts.save()
	return redirect('/users/settings/')

def change_password(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if request.method == 'POST':
		from django.contrib.auth.hashers import check_password
		data = request.POST
		form = ChangePasswordForm(request.POST)
		if form.is_valid() and check_password(data['password_old'], request.user.password) and data['password_new'] == data['password_new2'] and len(data['password_new']) >= 6:
			user = User.objects.get(id = request.user.id)
			user.set_password(data['password_new'])
			user.save()	
			return redirect('/auth/in')			
	redirect('/users/settings/?error_password=1')