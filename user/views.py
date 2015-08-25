from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.forms import PasswordChangeForm
from timetable.utils import avatar, pointsumm, getrank, handle_uploaded_file
from achievements.models import Action, Achievement, AchUnlocked
from timetable.utils import addAction, setAch, checkAchievements
from .forms import *
import pymorphy2

# Create your views here.
def profile(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		checkAchievements(request.user)
		user = User.objects.get(id = id)
		username = user.first_name + ' ' + user.last_name
		avt = avatar(user)
		morph = pymorphy2.MorphAnalyzer()

		points = pointsumm(user)
		points_morph = morph.parse('очко')[0]

		friends = []
		friends_list = User.objects.all().exclude(id = id)
		for friend in friends_list:
			current = {
				'user_id': friend.id,
				'username': '%s %s' % (friend.first_name, friend.last_name),
				'avatar': avatar(friend),
			}
			friends.append(current)

		act_list = Action.objects.all().filter(login = user).order_by('-pub_date')
		actions_morph = morph.parse('действие')[0]
		actions = []
		for action in act_list:		
			user = action.login		
			avt = avatar(user)
			cur_action = {
				'avatar': avt,
				'username': username,
				'user_id': user.id,
				'action_text': action.text,
				'pub_date': action.pub_date,
			}
			actions.append(cur_action)

		ach_counter_morph = morph.parse('достижение')[0]
		my_last_achievements = []
		#try:
		my_ach = AchUnlocked.objects.all().filter(login = user).order_by('-pub_date')
		last_achievements = my_ach[:5]
		for ach in last_achievements:
			my_last_achievements.append({
				'title': ach.ach_id.title,
				'icon': ach.ach_id.icon,
				'description': ach.ach_id.description,
			})
		#except ObjectDoesNotExist:
		#	my_ach = []

		#получение звания пользователя
		rank = getrank(user)

		#получение удобочитаемого номера
		last_phone = user.userprofile.phone
		phone = '+7 (%s)-%s-%s-%s' % (last_phone[0:3], last_phone[3:6], last_phone[6:8], last_phone[8:10])

		context = {
			'title': username,
			'user': user,
			'bodyclass': 'profile-page',
			'avatar': avt,
			'friends': friends,
			'actions': actions,
			'active_page': 1,
			'actions_morph': actions_morph.make_agree_with_number(len(act_list)).word,
			'xp': points,
			'xp_morph': points_morph.make_agree_with_number(points).word,
			'ach_counter': len(my_ach),
			'ach_counter_morph': ach_counter_morph.make_agree_with_number(len(my_ach)).word,
			'last_achievements': my_last_achievements,
			'rank': rank,
			'contacts': user.userprofile,
			'phone': phone,
		}
		return render(request, 'profile.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def achievements(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		user = User.objects.get(id = id)
		username = user.first_name + ' ' + user.last_name
		avt = avatar(user)
		morph = pymorphy2.MorphAnalyzer()

		points = pointsumm(user)
		points_morph = morph.parse('очко')[0]

		friends = []
		friends_list = User.objects.all().exclude(id = id)
		for friend in friends_list:
			current = {
				'user_id': friend.id,
				'username': '%s %s' % (friend.first_name, friend.last_name),
				'avatar': avatar(friend),
			}
			friends.append(current)

		act_list = Action.objects.all().filter(login = user).order_by('-pub_date')
		actions_morph = morph.parse('действие')[0]
		actions = []
		for action in act_list:				
			cur_action = {
				'action_text': action.text,
			}
			actions.append(cur_action)

		ach_counter_morph = morph.parse('достижение')[0]
		try:
			my_ach_list = AchUnlocked.objects.all().filter(login = user).order_by('-pub_date')
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

		#получение звания пользователя
		rank = getrank(user)

		#получение удобочитаемого номера
		last_phone = user.userprofile.phone
		phone = '+7 (%s)-%s-%s-%s' % (last_phone[0:3], last_phone[3:6], last_phone[6:8], last_phone[8:10])

		context = {
			'title': username,
			'user': user,
			'bodyclass': 'profile-page',
			'avatar': avt,
			'friends': friends,			
			'active_page': 2,
			'actions_morph': actions_morph.make_agree_with_number(len(act_list)).word,
			'xp': points,
			'actions': actions,
			'xp_morph': points_morph.make_agree_with_number(points).word,
			'my_ach': my_ach,
			'achs': achs,
			'ach_counter': len(my_ach),
			'ach_counter_morph': ach_counter_morph.make_agree_with_number(len(my_ach)).word,
			'rank': rank,			
			'contacts': user.userprofile,
			'phone': phone,
		}
		return render(request, 'profile-achievements.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def settings(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
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
		if form.is_valid():
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