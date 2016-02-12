from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from timetable.utils import avatar, pointsumm, getrank, handle_uploaded_file
from achievements.models import Action, Achievement, AchUnlocked#, Notification
from timetable.utils import addAction, setAch, checkAchievements, isOnline, UpdateStatus, setBonusPoints, bingo
from timetable.models import Lesson_Item
from notes.models import Note
from polls.models import Question
from events.models import Event
from inventory.models import *
from .forms import *
from .models import *
from .utils import getProfileInfo
import pymorphy2
import datetime

# Create your views here.
def profile(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		#Бонусные очки
		bonus = setBonusPoints(request.user)	
		_bingo = bingo(request.user)

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
			'attendance_percent': up['attendance_percent'],
			'duties_percent': up['duties_percent'],
			'bonus': bonus,
			'level': up['level'],
			'percent': up['percent'],
			'bingo': _bingo,
			'more': up,
		}
		return render(request, 'profile.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def achievements(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		_bingo = bingo(request.user)
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
			'attendance_percent': up['attendance_percent'],
			'duties_percent': up['duties_percent'],
			'level': up['level'],
			'percent': up['percent'],
			'bingo': _bingo,
			'more': up,
		}
		return render(request, 'profile-achievements.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def user_content(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		_bingo = bingo(request.user)
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
			'attendance_percent': up['attendance_percent'],
			'duties_percent': up['duties_percent'],
			'level': up['level'],
			'percent': up['percent'],
			'bingo': _bingo,
			'more': up,
		}
		return render(request, 'profile_content.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def my_attendance(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		_bingo = bingo(request.user)
		UpdateStatus(request.user)
		checkAchievements(request.user)	
		up = getProfileInfo(id)	
		semester = settings.SEMESTER

		attendance = []
		for lesson in Lesson_Item.objects.all().filter(semester = semester):
			my_visits = []
			for day in Attendance.objects.all().filter(lesson = lesson).filter(Q(group = 0) | Q(group = (up['user'].userprofile.group))):
				type = 'Лекция'
				if day.type == 2: type = 'Практика'
				elif day.type == 3: type = 'Лабораторная работа'
				
				my_visits.append({
					'date': day.date,
					'type': type,
					'visitor': day.visitor,
				})
			attendance.append({
				'title': lesson.title,
				'days': my_visits,
			})

		context = {
			'title': up['title'],
			'user': up['user'],
			'bodyclass': 'profile-page',
			'avatar': up['avatar'],
			'friends': up['friends'],
			'actions': up['actions'],
			'active_page': 4,
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
			'attendance': attendance, 
			'attendance_percent': up['attendance_percent'],
			'duties_percent': up['duties_percent'],
			'level': up['level'],
			'percent': up['percent'],
			'bingo': _bingo,
			'more': up,
		}
		return render(request, 'profile_attendance.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def my_duties(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		_bingo = bingo(request.user)
		UpdateStatus(request.user)
		checkAchievements(request.user)	
		up = getProfileInfo(id)	
		semester = settings.SEMESTER

		duties = []
		for lesson in Lesson_Item.objects.all().filter(semester = semester):
			my_visits = []
			for day in Duty.objects.all().filter(lesson = lesson).filter(Q(group = 0) | Q(group = (up['user'].userprofile.group))):				
				my_visits.append({
					'id': day.id,
					'date': day.date,
					'description': day.description,
					'visitor': day.visitors,
				})
			duties.append({
				'title': lesson.title,
				'days': my_visits,
			})

		context = {
			'title': up['title'],
			'user': up['user'],
			'bodyclass': 'profile-page',
			'avatar': up['avatar'],
			'friends': up['friends'],
			'actions': up['actions'],
			'active_page': 5,
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
			'duties': duties, 
			'attendance_percent': up['attendance_percent'],
			'duties_percent': up['duties_percent'],
			'level': up['level'],
			'percent': up['percent'],
			'bingo': _bingo,
			'more': up,
		}
		return render(request, 'profile_duties.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def inventory(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	
	_bingo = bingo(request.user)
	UpdateStatus(request.user)
	up = getProfileInfo(id)	

	#Узнаем ID катапульты
	catapult = Item.objects.get(title = 'Подаркопульта')
	catapult_id = catapult.id
	has_catapult = False

	#Подсчитываем сумму предметов из инвентаря
	inventory_summ = 0

	#Получаем значение фильтра
	filter = 1
	data = request.GET
	filter_get = data.get('sort', False)
	if filter_get == 'price':
		filter = 2
		items = UserInventoryItem.objects.all().filter(user = up['user']).filter(stolen = False).order_by('price')
	elif filter_get == 'items':
		filter = 3
		items = UserInventoryItem.objects.all().filter(user = up['user']).filter(stolen = False).order_by('-item_id', 'price')
	elif filter_get == 'quality':
		filter = 4
		items = UserInventoryItem.objects.all().filter(user = up['user']).filter(stolen = False).order_by('quality', 'price')
	elif filter_get == 'type':
		filter = 5
		items = UserInventoryItem.objects.all().filter(user = up['user']).filter(stolen = False).order_by('-type', '-id')	
	else:
		items = UserInventoryItem.objects.all().filter(user = up['user']).filter(stolen = False).order_by('-id')

	inventory = []	
	for item in items:
		type = 'Обычный предмет'
		quality = 'Низкое качество'
		quality_class = ''
		thing = 0
		if item.type == 1:
			thing = Item.objects.get(pk = item.item_id)
		elif item.type == 2:
			thing = Background.objects.get(pk = item.item_id)
			type = 'Фон профиля'
		elif item.type == 3:
			thing = SmileCollection.objects.get(pk = item.item_id)
			type = 'Набор смайликов'

		if item.quality == 2: 
			quality = 'Высокое качество'
			quality_class = 'high'
		elif item.quality == 3: 
			quality = 'Эксклюзивная вещь'
			quality_class = 'exclusive'

		if item.item_id == catapult_id:
			has_catapult = True

		no_sold = False
		is_catapult = False
		if thing.no_sold:				
			no_sold = True
			is_catapult = True

		inventory_summ += item.price

		inventory.append({
			'id': item.id,
			'title': thing.title,
			'icon': thing.icon.url,
			'quality': quality,
			'quality_class': quality_class,
			'type': type,
			'price': item.price,
			'no_sold': no_sold,
			'is_catapult': is_catapult,
		})

	context = {
		'title': up['title'],
		'user': up['user'],
		'bodyclass': 'profile-page',
		'avatar': up['avatar'],
		'friends': up['friends'],
		'actions': up['actions'],
		'active_page': 6,
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
		'inventory': inventory, 
		'has_catapult': has_catapult,
		'inventory_summ': inventory_summ,
		'inventory_count': len(inventory),
		'filter': filter,
		'attendance_percent': up['attendance_percent'],
		'duties_percent': up['duties_percent'],
		'level': up['level'],
		'percent': up['percent'],
		'bingo': _bingo,
		'more': up,
	}
	return render(request, 'profile_inventory.html', context)

def collection(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	
	_bingo = bingo(request.user)
	UpdateStatus(request.user)
	up = getProfileInfo(id)	

	#Получаем количество элементов
	collections_list = ItemCollection.objects.all().order_by('-id')
	collections = []
	
	for collection in collections_list:
		items_in_collection = []
		for item in collection.items.all():
			user_has_this_item = False
			if UserInventoryItem.objects.filter(user = request.user, type = 1, item_id = item.id, quality = 3, stolen = False).exists():
				user_has_this_item = True
			items_in_collection.append({
				'image': item.icon.url,
				'title': item.title,
				'user_has_this_item': user_has_this_item
				});
		collection_complete = True
		for item in items_in_collection:
			if item['user_has_this_item'] == False:
				collection_complete = False
				break

		collections.append({
			'title': collection.title,
			'items': items_in_collection,
			'complete': collection_complete
			})

	print(collections)

	
	context = {
		'title': up['title'],
		'user': up['user'],
		'bodyclass': 'profile-page',
		'avatar': up['avatar'],
		'friends': up['friends'],
		'actions': up['actions'],
		'active_page': 6,
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
		'collections': collections,
		'attendance_percent': up['attendance_percent'],
		'duties_percent': up['duties_percent'],
		'level': up['level'],
		'percent': up['percent'],
		'bingo': _bingo,
		'more': up,
	}
	return render(request, 'profile_collection.html', context)

	
def statistic(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	from django.db.models import Sum
	try:
		_bingo = bingo(request.user)
		UpdateStatus(request.user)
		checkAchievements(request.user)	
		up = getProfileInfo(id)	

		items_count = UserInventoryItem.objects.filter(user = up['user']).count()
		items_price = UserInventoryItem.objects.filter(user = up['user']).aggregate(Sum('price'))
		items_exclusives = UserInventoryItem.objects.filter(user = up['user']).filter(quality = 3).count()
		catapult_count = Catapult.objects.filter(from_user = up['user']).count()

		general_stats = {
			'items_count': items_count,
			'items_price': items_price,
			'items_exclusives': items_exclusives,
			'catapult_count': catapult_count,
		}

		items_stats = []
		for item in Item.objects.all():
			item_count = UserInventoryItem.objects.filter(user = up['user']).filter(item_id = item.id).count()
			item_price = (UserInventoryItem.objects.filter(user = up['user']).filter(item_id = item.id).aggregate(Sum('price')))['price__sum']
			if item_price == None: 
				item_price = 0
			item_catapults = Catapult.objects.filter(from_user = up['user']).filter(item__item_id = item.id).count()
			count_low = UserInventoryItem.objects.filter(user = up['user']).filter(item_id = item.id).filter(quality = 1).count()
			count_high = UserInventoryItem.objects.filter(user = up['user']).filter(item_id = item.id).filter(quality = 2).count()
			count_exclusive = UserInventoryItem.objects.filter(user = up['user']).filter(item_id = item.id).filter(quality = 3).count()
			items_stats.append({
				'icon': item.icon.url,
				'title': item.title,
				'count': item_count,
				'price': item_price,
				'catapults': item_catapults,
				'low': count_low,
				'high': count_high,
				'exclusive': count_exclusive,
			})

		context = {
			'title': up['title'],
			'user': up['user'],
			'bodyclass': 'profile-page',
			'avatar': up['avatar'],
			'friends': up['friends'],
			'actions': up['actions'],
			'active_page': 7,
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
			'attendance_percent': up['attendance_percent'],
			'general_stats': general_stats,
			'items_stats': items_stats,
			'duties_percent': up['duties_percent'],
			'level': up['level'],
			'percent': up['percent'],
			'bingo': _bingo,
			'more': up,
		}
		return render(request, 'profile_stats.html', context)
	except ObjectDoesNotExist:
		return redirect('/')

def user_settings(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	UpdateStatus(request.user)
	avatar_upload = UploadAvatarForm()
	change_password = ChangePasswordForm()
	set_contacts = SetContactForm(initial = {'vk': request.user.userprofile.vk, 'facebook': request.user.userprofile.facebook, 'twitter': request.user.userprofile.twitter, 'phone': request.user.userprofile.phone})
	error_password = request.GET.get('error_password', False)
	context = {
		'title': 'Настройки (beta)',
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

def addNotification(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	error = [False, '']
	form = AddNotificationForm()	
	if request.method == 'POST':
		data = request.POST
		form = AddNotificationForm(data)	
		print(data)
		if form.is_valid():
			for notif in data['aims']:
				print(notif)
				user = User.objects.get(username = notif)				
				notification = Notification()
				notification.login = user
				notification.author = user.username
				notification.title = data['title']
				notification.text = data['text']
				notification.is_anon = data.get('is_anon', False)
				notification.save()
			return redirect('/')
		else:
			error_message = 'Произошла ошибка'
			if (len(data['title']) < 2 or len(data['context']) < 2): error_message = 'Длина заголовка и текста уведомления должна быть более 2-х символов'	
			if not data['aims']: error_message = 'Не выбран ни один пользователь'
			error[0] = True
			error[1] = error_message
	context = {
		'title': 'Выслать уведомление',
		'form': form,
		'error': error[0],
		'error_message': error[1],
	}
	return render(request, 'send_notification.html', context)

def duty_done(request):
	if request.method == 'GET':
		data = request.GET
		id = data.get('duty', False)
		if id:
			duty = Duty.objects.get(pk = id)
			duty.visitors.add(request.user)
			duty.save()
	return redirect('/users/duty/%s' % (request.user.id))	

def save_additional(request):
	if request.method == 'GET':
		data = request.GET
		beta = data.get('beta', False)
		hide_email = data.get('hide_email', False)

		request.user.userprofile.beta = beta
		request.user.userprofile.hide_email = hide_email
		
		request.user.userprofile.save()
	return redirect('/users/settings/')	

@csrf_exempt
def sold_inventory_item(request):
	from user.models import UserProfile	
	user = UserProfile.objects.get(user = request.user)

	if request.method == 'POST':
		data = request.POST
		item_id = data.get('id', False)
		if item_id:
			useritem = UserInventoryItem.objects.get(pk = item_id)
			if not useritem.stolen:
				user.bonus_points += useritem.price
			useritem.stolen = True
			useritem.save()

			user_item_text = ''
			item = Item.objects.get(pk = useritem.item_id)
			if useritem.quality == 1:
				user_item_text = "<span class='quality-1'>"
			elif useritem.quality == 2:
				user_item_text = "<span class='quality-2'>"
			elif useritem.quality == 3:
				user_item_text = "<span class='quality-3'>"
			user_item_text = user_item_text + item.title + "</span>" 
			

			user.save()
			addAction(request.user, 'продал %s из инвентаря за %s <i class="trophy icon"></i>' % (user_item_text, useritem.price,), False)		
			
			request.user.userprofile.save()
			return HttpResponse('ok', content_type='text/html')	
		return HttpResponse('ss' + item_id + 's', content_type='text/html')	
	return HttpResponse('no', content_type='text/html')	


def lottery(request):
	import random
	from timetable.utils import pointsumm, getRandomItem
	if pointsumm(request.user) >= 17:
		items = []
		for i in range(1, 13):
			items.append({
				'id': i,
				'item': getRandomItem(),
				})
		prize = random.randint(0, 11)
		userGetItem = UserInventoryItem()
		userGetItem.user = request.user
		userGetItem.type = 1
		userGetItem.item_id = items[prize]['item']['item'].id
		userGetItem.price = items[prize]['item']['price']
		userGetItem.quality = items[prize]['item']['quality'] + 1
		userGetItem.save()
		index = prize;

		from user.models import UserProfile
		user = UserProfile.objects.get(user = request.user)
		user.bonus_points -= 17
		user.save()

		context = {
			'items': items,
			'index': index + 1,
			'prize': items[prize],
		}
		return render(request, 'lottery.html', context)
	else:
		return redirect('/users/inventory/%s' % (request.user.id,))	

def complect(request):
	import random
	from timetable.utils import pointsumm, getRandomItem
	if pointsumm(request.user) >= 99:
		items = []
		for i in range(1, 7):
			item = getRandomItem()
			inventoryItem = UserInventoryItem()
			inventoryItem.user = request.user
			inventoryItem.type = 1
			inventoryItem.item_id = item['item'].id
			inventoryItem.quality = item['quality'] + 1
			inventoryItem.price = item['price']
			inventoryItem.save()

			quality = 'Низкое качество'
			quality_class = ''			

			if item['quality'] == 1: 
				quality = 'Высокое качество'
				quality_class = 'high'
			elif item['quality'] == 2: 
				quality = 'Эксклюзивная вещь'
				quality_class = 'exclusive'

			items.append({
				'id': i,
				'item': item,
				'quality_class': quality_class,
				'quality': quality,
				})

		from user.models import UserProfile
		user = UserProfile.objects.get(user = request.user)
		user.bonus_points -= 99
		user.save()

		context = {
			'items': items,
		}
		return render(request, 'complect.html', context)
	else:
		return redirect('/users/inventory/%s' % (request.user.id,))	

@csrf_exempt 
def send_catapult(request):
	import random
	if request.method == 'POST':
		data = request.POST
		item_id = data.get('item_id', False)
		if item_id:
			item = UserInventoryItem.objects.get(id = item_id)
			if item.stolen:
				return HttpResponse('no', content_type='text/html')

			users = User.objects.all().exclude(id = request.user.id).filter(is_active = True)
			rand_user = random.choice(users)

			new_item = UserInventoryItem()
			new_item.user = rand_user
			new_item.type = item.type
			new_item.item_id = item.item_id
			new_item.quality = item.quality
			new_item.price = item.price
			new_item.save()

			#Узнаем ID катапульты и убираем ее из инвентаря
			catapult_quality = 1
			catapult = Item.objects.get(title = 'Подаркопульта')
			catapult_id = catapult.id
			my_catapultes = UserInventoryItem.objects.all().filter(item_id = catapult_id).filter(user = request.user).filter(stolen = False).latest('id')
			if my_catapultes.quality == 2:
				catapult_quality = 2
			if my_catapultes.quality == 3:
				catapult_quality = 3
			my_catapultes.stolen = True
			my_catapultes.save()

			item.stolen = True
			item.save()

			catapult = Catapult()
			catapult.from_user = request.user
			catapult.to_user = rand_user
			catapult.item = new_item
			catapult.save()

			#Прибавляем очки пользователю
			from user.models import UserProfile	
			user = UserProfile.objects.get(user = request.user)

			catapult_text = "<span class='quality-%s'>подаркопульту</span>" % (catapult_quality,)
			if catapult_quality == 1:								
				if item.quality == 1:
					user.bonus_points += 5
				if item.quality == 2:
					user.bonus_points += 15
				if item.quality == 3:
					user.bonus_points += 25
			elif catapult_quality == 2:
				if item.quality == 1:
					user.bonus_points += 15
				if item.quality == 2:
					user.bonus_points += 35
				if item.quality == 3:
					user.bonus_points += 50
			elif catapult_quality == 3:				
				if item.quality == 1:
					user.bonus_points += 30
				if item.quality == 2:
					user.bonus_points += 55
				if item.quality == 3:
					user.bonus_points += 100

			db_item = Item.objects.get(pk = item.item_id)
			user_item_text = '<span class="quality-%s">%s</span>' % (item.quality, db_item.title,)

			user.save()

			addAction(request.user, 'запустил %s и бросил %s в <b>%s</b>' % (catapult_text, user_item_text, rand_user.get_full_name(),), False)
			return HttpResponse('%s' % (rand_user.get_full_name(),), content_type='text/html')
		return HttpResponse('no', content_type='text/html')
	else:
		return HttpResponse('no', content_type='text/html')

'''def run_distribution(request):
	if request.user.is_superuser:
		import random

		users = User.objects.all()
		for user in users:
			items_ = []
			for i in range(1, 3):
				item = getRandomItem()
				quality = 'Низкое качество'
				if item['quality'] == 1:
					quality = 'Высокое качество'
				elif item['quality'] == 2:
					quality = 'Эксклюзивное качество'

				items.append({
					'item': item,
					'quality': quality,
				})

			catapult_quality = 1
			rnd = random.random()
			if rnd >= 0.7:
				catapult_quality = 2
			if rnd >= 0.95:
				catapult_quality = 3'''

def open_case(request, id):
	import random
	try:
		item = UserInventoryItem.objects.get(pk = id)
		case = Item.objects.get(pk = item.item_id)
		if item.stolen == True:
			return redirect('/users/inventory/%s' % (request.user.id,))	
		items = []
		gramms = 5
		
		max = random.choice(2, 4)
		if item.quality == 1:
			for i in range(2, max + 1):
				item = getRandomItem()
				items.append({
					'item': item.item,
					'quality': item.quality,
					'price': item.price,
				})

	except Item.DoesNotExists:
		return redirect('/users/inventory/%s' % (request.user.id,))	