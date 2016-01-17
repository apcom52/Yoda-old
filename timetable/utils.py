from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from achievements.models import Action, AchUnlocked, Rank, Achievement#, Notification
from django.contrib.auth.models import User
from django.utils import timezone
from user.models import *
from polls.models import QueAns
from events.models import UserVisitEvent
from inventory.models import Item, UserInventoryItem #Smile, SmileCollection
import datetime

class DTControl:
	def __init__(self):
		self.today = datetime.datetime.today()
		self.now = datetime.datetime.now()
		self.year = self.today.year
		self.month = self.today.month
		self.weekday = self.today.weekday() + 1
		self.day = self.today.day
		self.weeknumber = datetime.date(self.year, self.month, self.day).isocalendar()[1]
		self.week = 1
		if (self.weeknumber + settings.WEEK_SHIFT) % 2 == 0: self.week = 2
		self.hour = self.now.hour
		self.minute = self.now.minute
		self.timesumm = self.hour * 60 + self.minute

	def gettimesummstart(self, lessonnum):
		if lessonnum == 1: return 500
		elif lessonnum == 2: return 600
		elif lessonnum == 3: return 705
		elif lessonnum == 4: return 840
		elif lessonnum == 5: return 945
		elif lessonnum == 6: return 1040
		elif lessonnum == 7: return 1135

	def gettimesummend(self, lessonnum):
		if lessonnum == 1: return 590
		elif lessonnum == 2: return 690
		elif lessonnum == 3: return 795
		elif lessonnum == 4: return 930
		elif lessonnum == 5: return 1035
		elif lessonnum == 6: return 1130
		elif lessonnum == 7: return 1225

	def ifpause(self, time):
		pauses = [[590, 600], [690, 705], [795, 840], [930, 945], [1035, 1040], [1130, 1135]]
		for p in pauses:
			if time < p[1] and time > p[0]: return True
		return False

	def getTimeFromNum(self, lessonnum):
		if lessonnum == 1: return '8:20'
		elif lessonnum == 2: return '10:00'
		elif lessonnum == 3: return '11:45'
		elif lessonnum == 4: return '14:00'
		elif lessonnum == 5: return '15:45'
		elif lessonnum == 6: return '17:20'
		elif lessonnum == 7: return '18:55'

def dateInfo(info):
	date = datetime.datetime(info['year'], info['month'], info['day'])
	weekday = date.weekday() + 1
	weeknumber = date.isocalendar()[1]
	week = 1
	if (weeknumber + settings.WEEK_SHIFT) % 2 == 0: week = 2
	return {
		'weekday': weekday,
		'weeknumber': weeknumber,
		'week': week,
		'date': date,
	}

def addAction(user, action_text, importance = True):
	action = Action()
	action.login = user
	action.text = action_text
	action.important = importance
	action.save()

def avatar(user):
	try:
		avatar = user.userprofile.avatar.url
	except ObjectDoesNotExist:
		return settings.NO_AVATAR
	return avatar

def pointsumm(user):
	summ = 0
	actions_list = Action.objects.all().filter(login = user)
	try:
		my_ach_list = AchUnlocked.objects.all().filter(login = user)
		for ach in my_ach_list:
			summ += ach.ach_id.xp
	except ObjectDoesNotExist:
		pass
	summ += actions_list.count()

	#Прибавляем еще кол-во голосований и походов на мероприятия
	my_votes = QueAns.objects.all().filter(login = user)
	my_visits = UserVisitEvent.objects.all().filter(login = user)
	summ += my_votes.count() + my_visits.count()

	#Прибавляем бонусные очки
	bonus = user.userprofile.bonus_points
	summ += bonus

	return summ

def getrank(user):
	if user: 
		actions = Action.objects.all().filter(login = user)
		summ = len(actions)
	rank = '???'
	try:
		rank_list = Rank.objects.get(start_points__lte = summ, end_points__gte = summ)
		rank = rank_list.rank
	except ObjectDoesNotExist:
		rank = '???'
	return rank

def setAch(user, id):
	try:
		achievement = Achievement.objects.get(id = id)
		if not AchUnlocked.objects.filter(login = user, ach_id = achievement).exists():
			user_unlock = AchUnlocked()
			user_unlock.login = user
			user_unlock.ach_id = achievement
			user_unlock.save()
			addAction(user, 'получил достижение<div class="comments"><div class="comment"><span class="avatar"><img src="%s"></span><div class="content"><span class="author">%s</span><div class="text">%s</div></div></div></div>' % (achievement.icon, achievement.title, achievement.description))
	except ObjectDoesNotExist:
		pass

def handle_uploaded_file(f):
	now = timezone.now()
	url = '/media/img/%s/%s/%s%s%s' % (now.year, now.month, now.day, now.hour, now.minute)
	with open(url, 'wb+') as destination:
		for chunck in f.chunck():
			destination.write(chunk)
			user = request.user
			user.userprofile.avatar = url
			user.save()

def checkAchievements(user, params = ['404', 'actives', 'admin', 'comments', 'visiter', 'contacts', '228']):
	if '404' in params:
		summ = pointsumm(user)
		if summ >= 404:
			setAch(user, 16)
	if 'actives' in params:
		actions = Action.objects.all().filter(login = user)
		summ = len(actions)
		if summ >= 75:
			setAch(user, 15)
		elif summ >= 25 and summ < 75:
			setAch(user, 10)
		elif summ >= 10 and summ < 25:
			setAch(user, 5)
	if 'admin' in params:
		if getrank(user) == 'Шаман':
			setAch(user, 12)
	if 'comments' in params:
		from notes.models import NoteComment
		from polls.models import PollComment
		comments_notes = NoteComment.objects.all().filter(login = user).count()
		comments_polls = PollComment.objects.all().filter(login = user).count()
		summ = comments_notes + comments_polls
		if summ >= 5 and summ <= 24:
			setAch(user, 7)
		elif summ >= 25:
			setAch(user, 26)

	if 'visiter' in params:
		from events.models import UserVisitEvent
		events_visit = UserVisitEvent.objects.all().filter(login = user).count()
		if events_visit >= 3:
			setAch(user, 13)
	if 'contacts' in params:
		from user.models import UserProfile
		my_profile = UserProfile.objects.get(user = user)
		if my_profile.vk or my_profile.facebook or my_profile.twitter:
			setAch(user, 9)
		if my_profile.phone:
			setAch(user, 11)
	if '404' in params:
		summ = pointsumm(user)
		if summ >= 228:
			setAch(user, 27)

def getTimetable(semester = settings.SEMESTER, week = 1, day = 1, date = ''):
	from .models import Lesson, Teacher, Timetable, Homework, Control, NewPlace, TeacherTimetable, NotStudyTime, TransferredLesson, CanceledLesson
	is_weekend = False
	try:
		sc = NotStudyTime.objects.filter(start_date__lte = datetime.date.today()).filter(end_date__gte = datetime.date.today())		
		if len(sc) > 0: is_weekend = True
	except ObjectDoesNotExist:
		return -1

	today = DTControl()	
	timetable = []	
	tm_list = Timetable.objects.all().filter(semester = semester, week = week, day = day)
	for lesson in tm_list:
		title = lesson.lesson.title
		lesson_is_end = False
		try:
			teacher_avatar = lesson.teacher.avatar.url
		except ValueError:
			teacher_avatar = '/media/img/2015/08/04/ufo.jpg'
		result_time = lesson.time
		if lesson.double: result_time += 1
		if today.gettimesummend(result_time) < today.timesumm: lesson_is_end = True
		type = 'Лекция'; type_color = 'olive'
		if lesson.lesson.type == 2: type='Практика'; type_color = 'blue'
		elif lesson.lesson.type == 3: type='Лабораторная работа'; type_color = 'red'

		now = datetime.date.today()
		today_date = now.strftime("%Y-%m-%d")
		#Проверка на наличие контрольной на этой паре
		has_control = False
		control = ''
		try:
			ctrl = Control.objects.get(date = date, time = lesson.time)
			control = ctrl.info
			has_control = True
		except ObjectDoesNotExist:
			pass

		#Проверка на наличие домашнего задания
		homework = False
		try:
			hw = Homework.objects.get(date = date, time = lesson.time)
			homework = hw.homework
		except ObjectDoesNotExist:
			pass
		
		#проверка на смену аудитории
		changePlace = False
		try:
			new_place = NewPlace.objects.get(date = date, time = lesson.time)
			place = new_place.new_place
			changePlace = new_place.new_place
		except ObjectDoesNotExist:
			pass

		#Проверка на перенос пары
		is_transfered = False
		try:
			new_lesson_tr = TransferredLesson.objects.get(last_date = date, last_time = lesson.time)
			is_transfered = {
				'place': new_lesson_tr.new_place,
				'date': new_lesson_tr.new_date,
				'lesson': new_lesson_tr.new_time,
			}
		except ObjectDoesNotExist:
			pass

		cur_lesson = {
			'title': lesson.lesson.title,
			'teacher': lesson.teacher.name,
			'teacher_id': lesson.teacher.id,
			'teacher_avatar': teacher_avatar,
			'type': type,
			'type_color': type_color,
			'num': int(lesson.time),
			'is_end': lesson_is_end,
			'start_time': today.getTimeFromNum(lesson.time),
			'place': lesson.place,
			'double': lesson.double,
			'has_control': has_control,
			'control': control,
			'homework': homework,
			'changePlace': changePlace,		
			'is_transfered': is_transfered,
			'is_canceled': False,
		}

		timetable.append(cur_lesson)

	#Получение перенесенных пар
	new_lesson_tr = TransferredLesson.objects.all().filter(new_date = date)
	new_timetable = []
	for new_lesson in new_lesson_tr:
		lesson = new_lesson.lesson
		title = lesson.lesson.title
		lesson_is_end = False
		try:
			teacher_avatar = lesson.teacher.avatar.url
		except ValueError:
			teacher_avatar = '/media/img/2015/08/04/ufo.jpg'
		result_time = lesson.time
		if lesson.double: result_time += 1
		if today.gettimesummend(result_time) < today.timesumm: lesson_is_end = True
		type = 'Лекция'; type_color = 'olive'
		if lesson.lesson.type == 2: type='Практика'; type_color = 'blue'
		elif lesson.lesson.type == 3: type='Лабораторная работа'; type_color = 'red'

		now = datetime.date.today()
		today_date = now.strftime("%Y-%m-%d")
		#Проверка на наличие контрольной на этой паре
		has_control = False
		control = ''
		try:
			ctrl = Control.objects.get(date = date, time = lesson.time)
			control = ctrl.info
			has_control = True
		except ObjectDoesNotExist:
			pass

		#Проверка на наличие домашнего задания
		homework = False
		try:
			hw = Homework.objects.get(date = date, time = lesson.time)
			homework = hw.homework
		except ObjectDoesNotExist:
			pass

		cur_lesson = {
			'title': lesson.lesson.title,
			'teacher': lesson.teacher.name,
			'teacher_id': lesson.teacher.id,
			'teacher_avatar': teacher_avatar,
			'type': type,
			'type_color': type_color,
			'num': int(new_lesson.new_time),
			'is_end': lesson_is_end,
			'start_time': today.getTimeFromNum(new_lesson.new_time),
			'place': new_lesson.new_place,
			'double': lesson.double,
			'has_control': has_control,
			'control': control,
			'last_date': new_lesson.last_date,
			'is_canceled': False,
		}
		new_timetable.append(cur_lesson)

	#Получаем информацию об отмененных парах
	canceled_lessons_list = CanceledLesson.objects.all().filter(date = date)
	canceled_lessons = []
	for l in canceled_lessons_list:
		canceled_lessons.append({
			'num': l.time,
		})


	#Проходимся по списку перенесенных пар и заменяем текущие пары на них
	for tt in new_timetable:		
		for i, t in enumerate(timetable):
			if t['num'] == tt['num']:
				timetable[i] = tt
				break

	for tt in canceled_lessons:		
		for t in timetable:
			if t['num'] == tt['num']:
				t['is_canceled'] = True
				break	

	if len(timetable) == 0: return -1

	return timetable

def UpdateStatus(_user):
	from user.models import UserProfile
	user = UserProfile.objects.get(user = _user)
	user.last_visit = datetime.datetime.now()
	user.save()

def isOnline(_user):
	now = datetime.datetime.now()
	try:
		user_lv = _user.userprofile.last_visit
		user_last = datetime.datetime(user_lv.year, user_lv.month, user_lv.day, user_lv.hour, user_lv.minute)
		user_last += datetime.timedelta(hours = 3)
		if (now - user_last) <= datetime.timedelta(minutes = 10): return True
		return False
	except AttributeError:
		return False	

def getRandomItem(med = 0.7, high = 0.95):
	import random
	items = Item.objects.all()
	random_item = random.choice(items)

	qrnd = random.random()
	quality = 0
	if qrnd >= med:	quality = 1
	if qrnd >= high: quality = 2

	price = 0
	if quality == 0:
		old_price = random_item.price_low;
		price = random.randint(round(old_price / 4), old_price)
	elif quality == 1:
		old_price = random_item.price_med;
		price = random.randint(round(old_price / 3), old_price)
	elif quality == 2:
		old_price = random_item.price_high;
		price = random.randint(round(old_price / 2), old_price)

	return {
		'item': random_item,
		'quality': quality,
		'price': price,
	}

def setBonusPoints(_user):
	from user.models import UserProfile, BonusPoints

	user = UserProfile.objects.get(user = _user)
	now = datetime.datetime.now()

	last_bonus = BonusPoints.objects.all().filter(user = _user).filter(bingo = False).order_by('-date')	

	if last_bonus:
		user_lv = last_bonus[0].date
		user_last = datetime.datetime(user_lv.year, user_lv.month, user_lv.day, user_lv.hour, user_lv.minute)	
		user_last += datetime.timedelta(hours = 3)	
	bonus = 0
	pos = 0
	is_item = 0
	item1, item2 = getRandomItem(), getRandomItem()

	#Указываем индексы квадратиков для каждого бонуса:
	bonus_positions = [[2, 3, 8, 10, 14], [1, 7, 9, 12], [13, 16], [4, 5], [11], [15, 6]]
	if not last_bonus or now.day != user_last.day:
		import random
		rnd = random.random()		
		bonus = 1
		if rnd > 0.33:	
			bonus = 2
		if rnd > 0.54:	
			bonus = 3
		if rnd > 0.69:	
			bonus = 4
		if rnd > 0.8:	
			bonus = 5
		if rnd > 0.85:	
			pos = random.choice([6, 15])
			userGetItem = UserInventoryItem()
			userGetItem.user = _user
			userGetItem.type = 1
			if pos == 6:
				userGetItem.item_id = item1['item'].id
				userGetItem.price = item1['price']
				userGetItem.quality = item1['quality'] + 1
			else:
				userGetItem.item_id = item2['item'].id
				userGetItem.price = item2['price']
				userGetItem.quality = item2['quality'] + 1
			userGetItem.save()
			bonus = 0
			is_item = True

		if not is_item:
			user.bonus_points += bonus

		pos_array = bonus_positions[bonus - 1]
		if rnd <= 0.85: pos = random.choice(pos_array)

		bonusStat = BonusPoints()
		bonusStat.user = _user
		bonusStat.bonus = bonus
		bonusStat.save()

		user.save()
	return {
		'xp': bonus,
		'index': pos,
		'is_item': is_item,
		'item1': item1, 
		'item2': item2,
	}

def bingo(_user):
	from user.models import UserProfile, BonusPoints
	import random
	user = UserProfile.objects.get(user = _user)
	bonus = 0
	rnd = random.random()
	item1, item2, item3 = getRandomItem(), getRandomItem(), getRandomItem()
	index = 0
	is_item = False
	if rnd >= 0.99:
		rnd2 = random.random()
		positions = [1, 2, 4, 5, 7, 8, 9, 10, 11, 3, 6, 12]
		bonus = 0
		if rnd2 < 0.6:	
			bonus = random.randint(1, 9)
			user.bonus_points += bonus
			user.save()
			index = positions[bonus - 1]
		else:
			bonus = random.randint(10, 12)
			is_item = True
			index = positions[bonus - 1]
			bonus = 0

			userGetItem = UserInventoryItem()
			userGetItem.user = _user
			userGetItem.type = 1
			if index == 3:
				userGetItem.item_id = item1['item'].id
				userGetItem.price = item1['price']
				userGetItem.quality = item1['quality'] + 1
			elif index == 6:
				userGetItem.item_id = item2['item'].id
				userGetItem.price = item2['price']
				userGetItem.quality = item2['quality'] + 1
			elif index == 12:
				userGetItem.item_id = item3['item'].id
				userGetItem.price = item3['price']
				userGetItem.quality = item3['quality'] + 1
			userGetItem.save()


		bonusStat = BonusPoints()
		bonusStat.user = _user
		bonusStat.bonus = bonus
		bonusStat.bingo = True
		bonusStat.save()

		bonus_suffix = 'очко'
		if bonus >= 2 and bonus <= 4: bonus_suffix = 'очка'
		if bonus >= 5: bonus_suffix = 'очков'


		if bonus:
			addAction(_user, 'получил <b>Случайный бонус (%s %s)</b>' % (bonus, bonus_suffix), False)
		else:
			addAction(_user, 'получил случайный бонус (предмет из инвентаря)', False)

		bingo = {		
			'xp': bonus, 
			'index': index,
			'is_item': is_item,
			'item1': item1,
			'item2': item2,
			'item3': item3,
		}
		return bingo
	else:
		return 0	

def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60 
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)


'''def parseSmiles(text):
	smiles = Smile.objects.all()
	for smile in smiles:
		text = text.replace(":|%s|:" % (smile.symbol,), "<img src='%s'>" % (smile.icon.url,))
	return text'''

'''def getNotifications(user):
	notifications_list = Notification.objects.all().filter(login = user)
	notifications = []
	for notification in notifications_list:
		user = None
		if not notification.is_anon:
			_user = User.objects.get(id = notification.author)
		notifications.append({
			'title': notification.title,
			'text': notification.text,
			'is_anon': notification.is_anon,
			'is_system': notification.is_system,
			'author': notification.author,
			'author_username': _user.first_name + ' ' + _user.last_name
		})
	return notifications'''
