from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from achievements.models import Action, AchUnlocked
from django.db.models.fields import related
from django.core.exceptions import ObjectDoesNotExist 
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Lesson, Teacher, Timetable, Homework, Control, NewPlace, TeacherTimetable, NotStudyTime
from events.models import Event, UserVisitEvent
from .utils import DTControl, addAction, checkAchievements
from .forms import *
import datetime

# Create your views here.
def index(request):
	#Получение списка новых достижений
	checkAchievements(request.user)
	page = request.GET.get('page', 1)
	
	new_achievements = []
	try:
		my_new_ach = AchUnlocked.objects.all().filter(login = request.user).filter(is_new = True)
		print(len(my_new_ach))		
		for ach in my_new_ach:
			ach.is_new = False
			ach.save()
			new_achievements.append({
				'title': ach.ach_id.title,
				'icon': ach.ach_id.icon,
				'description': ach.ach_id.description,
			})
	except ObjectDoesNotExist:
		new_achievements = []


	#Получение списка активностей	
	act_list = Action.objects.order_by('-pub_date').all()
	p = Paginator(act_list, 25)
	if int(page) < 1: page = 1
	elif int(page) > p.num_pages: page = p.num_pages
	current_page = p.page(page)
	actions_list = []
	for action in current_page.object_list:		
		user = action.login		
		try:
			avatar = user.userprofile.avatar.url
		except ObjectDoesNotExist:
			avatar = settings.NO_AVATAR
		cur_action = {
			'avatar': avatar,
			'username': user.first_name + ' ' + user.last_name,
			'userlogin': user.id,
			'action_text': action.text,
			'pub_date': action.pub_date,
		}
		actions_list.append(cur_action)

	#Получение информации о выходных
	is_weekend = False
	try:
		sc = NotStudyTime.objects.filter(start_date__lte = datetime.date.today()).filter(end_date__gte = datetime.date.today())		
		if len(sc) > 0: is_weekend = True
	except ObjectDoesNotExist:
		print('=== = = = I do not that!')
	
	#Получение списка предметов
	today = DTControl()	
	timetable = []	
	tm_list = Timetable.objects.all().filter(semester = settings.SEMESTER, week = today.week, day = today.weekday)
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
			ctrl = Control.objects.get(date = today_date, time = lesson.time)
			control = ctrl.info
			has_control = True
		except ObjectDoesNotExist:
			pass

		#Проверка на наличие домашнего задания
		homework = False
		try:
			hw = Homework.objects.get(date = today_date, time = lesson.time)
			homework = hw.homework
		except ObjectDoesNotExist:
			pass
		
		#проверка на смену аудитории
		changePlace = False
		try:
			new_place = NewPlace.objects.get(date = today_date, time = lesson.time)
			place = new_place.new_place
			changePlace = True
		except ObjectDoesNotExist:
			pass

		cur_lesson = {
			'title': lesson.lesson.title,
			'teacher': lesson.teacher.name,
			'teacher_id': lesson.teacher.id,
			'teacher_avatar': teacher_avatar,
			'type': type,
			'type_color': type_color,
			'num': lesson.time,
			'is_end': lesson_is_end,
			'start_time': today.getTimeFromNum(lesson.time),
			'place': lesson.place,
			'double': lesson.double,
			'has_control': has_control,
			'control': control,
			'homework': homework,
			'changePlace': changePlace,		
		}

		timetable.append(cur_lesson)

	#Получение списка мероприятий
	start_event_date = timezone.now()
	end_event_date = start_event_date + datetime.timedelta(days=10)
	events_list = Event.objects.all().filter(date__gte = start_event_date).filter(date__lte = end_event_date).order_by('date')
	events = []
	for event in events_list:
		opinion = False
		if event.is_required == False:
			try:
				you_opin = UserVisitEvent.objects.get(login = request.user, event = event)
				opinion = you_opin.answer
			except ObjectDoesNotExist: pass
		if opinion != 3:
			events.append({
				'id': event.id,
				'title': event.title,
				'date': event.date,
				'is_required': event.is_required,
				'description': event.description,
				'answer': opinion,
			})

	#Получение списка сегодняшних мероприятий (обязательных и тех, на которые подписался пользователь)
	time_now = timezone.now()
	end_time_now = time_now + datetime.timedelta(days = 1)
	my_canceled_events_list = UserVisitEvent.objects.all().filter(login = request.user, answer = 3)
	my_canceled_events = []
	for c in my_canceled_events_list: my_canceled_events.append(c.event.id)
	print(my_canceled_events)
	today_events_list = Event.objects.all().filter(date__gte = time_now).filter(date__lte = end_time_now).exclude(id__in = my_canceled_events)#filter(date__gte = end_time_now).filter(date__lte = my_canceled_events).exclude(id__in = my_canceled_events)
	today_events = []
	for event in today_events_list:
		opinion = False
		if event.is_required == False:
			try:
				you_opin = UserVisitEvent.objects.get(login = request.user, event = event)
				opinion = you_opin.answer
			except ObjectDoesNotExist: pass
		today_events.append({
			'id': event.id,
			'title': event.title,
			'date': event.date,
			'is_required': event.is_required,
			'answer': opinion,
		})

	context = {
		'title': 'Главная',
		'actions_list': actions_list,
		'timetable': timetable,
		'is_weekend': is_weekend,
		'new_achievements': new_achievements,
		'events': events,
		'today_events': today_events,
		'pagination': {
				'has_prev': current_page.has_previous(),
				'has_next': current_page.has_next(),
				'current': current_page.number,
				'prev': current_page.number - 1,
				'next': current_page.number + 1,
			}
	}
	return render(request, 'index.html', context)


def teacher(request, id):
	try:
		teacher = Teacher.objects.get(id = id)
		lessons = teacher.lessons.all()
		lessons_list = []
		try:
			avatar = teacher.avatar.url
		except ValueError:
			avatar = '/media/img/2015/08/04/ufo.jpg'

		for lesson in lessons:
			color = 'olive'
			if lesson.type == 2: color = 'blue'
			elif lesson.type == 3: color = 'red'
			current = {
				'title': lesson.title,
				'semester': lesson.semester,
				'color': color,
			}
			lessons_list.append(current)

		context = {
			'title': teacher.name, 
			'bodyclass': 'profile-page',
			'name': teacher.name,
			'lessons': lessons_list,
			'avatar': avatar,
			'teacher_id': teacher.id,
			'active_page': 1,
		}
		return render(request, 'teacher.html', context)
	except ObjectDoesNotExist:
		return redirect('/')


def all_timetable(request):
	weeks = []
	week1 = []
	week2 = []
	i = 1
	day = 1
	week = 1
	while i <= 6:
		lessons = Timetable.objects.all().filter(week = week, day = i)
		day = []
		if i == 1 or i == 7: dayname = 'Понедельник'
		elif i == 2 or i == 8: dayname = 'Вторник'
		elif i == 3 or i == 9: dayname = 'Среда'
		elif i == 4 or i == 10: dayname = 'Четверг'
		elif i == 5 or i == 11: dayname = 'Пятница'
		elif i == 6 or i == 12: dayname = 'Суббота'
		day.append({
			'title': dayname,
			'color': '',
		})
		last_id = 1
		for lesson in lessons:
			l = lesson.lesson
			while last_id != lesson.time:
				day.append({
					'title': '',
					'color': '',
				})
				last_id += 1

			color = 'olive'
			if l.type == 2: color = 'blue'
			elif l.type == 3: color = 'red'
			current = {
				'title': l.title, 
				'color': color,
			}
			day.append(current)
			if lesson.double:
				day.append(current)
				last_id += 1
			last_id += 1
		while len(day) <= 7:
			last_id += 1
			day.append({
				'title': '',
				'color': '',
			})
		if week == 1: week1.append(day)
		elif week == 2: week2.append(day)

		i += 1		
		if i == 7 and week == 1: 			
			week = 2
			i = 1	
	context = {
		'title': 'Расписание',
		'week1': week1,
		'week2': week2,
	}
	return render(request, 'timetable.html', context)


def add_homework(request):
	error = [False, '']
	form = AddHomeworkForm()	
	if request.method == 'POST':
		data = request.POST
		form = AddHomeworkForm(data)
		if form.is_valid():
			homework = Homework()
			homework.user = request.user
			homework.date = data['date']
			homework.time = data['time']
			homework.homework = data['homework']
			homework.save()
			try:
				set_date = data['date'].split('-')
				dt = datetime.date(int(set_date[0]), int(set_date[1]), int(set_date[2]))
				weekday = dt.isoweekday()
				weeknumber = int(dt.strftime('%U'))
				week = 1
				if (weeknumber + settings.WEEK_SHIFT) % 2 == 0: week = 2
				lesson = Timetable.objects.get(semester = settings.SEMESTER, week = week, day = weekday, time = data['time'])
				addAction(request.user, 'добавил домашнее задание по предмету "' + lesson.lesson.title + '"')			
			except ObjectDoesNotExist:
				addAction(request.user, 'добавил домашнее задание')
			return redirect('/')
		else:
			error_message = 'Произошла ошибка'
			if len(form['homework']) < 2: error_message = 'Длина сообщения о домашнем задании должна быть не менее 3-х символов'	
			error[0] = True
			error[1] = error_message
	context = {
		'title': 'Добавить домашнее задание',
		'form': form,
		'error': error[0],
		'error_message': error[1],
	}
	return render(request, 'add_homework.html', context)

def add_control(request):
	error = [False, '']
	form = AddControlForm()	
	if request.method == 'POST':
		data = request.POST
		form = AddControlForm(data)
		if form.is_valid():
			control = Control()
			control.user = request.user
			control.date = data['date']
			control.time = data['time']
			control.info = data['info']		
			control.save()	
			try:
				set_date = data['date'].split('-')
				dt = datetime.date(int(set_date[0]), int(set_date[1]), int(set_date[2]))
				weekday = dt.isoweekday()
				weeknumber = int(dt.strftime('%U'))
				week = 1
				if (weeknumber + settings.WEEK_SHIFT) % 2 == 0: week = 2
				lesson = Timetable.objects.get(semester = settings.SEMESTER, week = week, day = weekday, time = data['time'])
				addAction(request.user, 'добавил информацию о контрольной по предмету "' + lesson.lesson.title + '" в базу')	
			except ObjectDoesNotExist:
					addAction(request.user, 'добавил информацию о контрольной в базу')	
			return redirect('/')
		else:
			error[0] = True
			error[1] = 'Произошла ошибка при добавлении'
	context = {
		'title': 'Добавить контрольную',
		'form': form,
		'error': error[0],
		'error_message': error[1],
	}
	return render(request, 'add_control.html', context)

def change_place(request):
	error = [False, '']
	form = ChangePlaceForm()	
	if request.method == 'POST':
		data = request.POST
		form = ChangePlaceForm(data)
		if form.is_valid() and data['new_place']:
			try:
				has_changing = NewPlace.objects.get(date = data['date'], time = data['time'])
				has_changing.new_place = data['new_place']
				has_changing.save()
			except ObjectDoesNotExist:				
				newplace = NewPlace()
				newplace.user = request.user
				newplace.date = data['date']
				newplace.time = data['time']
				newplace.new_place = data['new_place']		
				newplace.save()	
			try:
				set_date = data['date'].split('-')
				dt = datetime.date(int(set_date[0]), int(set_date[1]), int(set_date[2]))
				weekday = dt.isoweekday()
				weeknumber = int(dt.strftime('%U'))
				week = 1
				if (weeknumber + settings.WEEK_SHIFT) % 2 == 0: week = 2
				lesson = Timetable.objects.get(semester = settings.SEMESTER, week = week, day = weekday, time = data['time'])
				addAction(request.user, 'изменил аудиторию "%s (%s.%s.%s - %s пара)" на %s' % (lesson.lesson.title, set_date[2], set_date[1], set_date[0], data['time'], data['new_place']))	
			except ObjectDoesNotExist:
				addAction(request.user, 'добавил информацию о смене аудитории')	
			return redirect('/')
		else:
			error[0] = True
			error[1] = 'Произошла ошибка при изменении аудитории'
	context = {
		'title': 'Изменить аудиторию',
		'form': form,
		'error': error[0],
		'error_message': error[1],
	}
	return render(request, 'change_place.html', context)



def teacher_timetable(request, id):	
	try:
		teacher = Teacher.objects.get(id = id)		
		try:
			avatar = teacher.avatar.url
		except ValueError:
			avatar = '/media/img/2015/08/04/ufo.jpg'
	except ObjectDoesNotExist:
		return redirect('/')

	week1 = []
	week2 = []
	i = 1
	day = 1
	week = 1
	while i <= 6:
		lessons = TeacherTimetable.objects.all().filter(teacher = teacher, week = week, day = i)
		day = []
		if i == 1 or i == 7: dayname = 'Понедельник'
		elif i == 2 or i == 8: dayname = 'Вторник'
		elif i == 3 or i == 9: dayname = 'Среда'
		elif i == 4 or i == 10: dayname = 'Четверг'
		elif i == 5 or i == 11: dayname = 'Пятница'
		elif i == 6 or i == 12: dayname = 'Суббота'
		day.append({
			'title': dayname,
			'color': '',
			'intersect': '',
		})
		last_id = 1
		for lesson in lessons:
			l = lesson.lesson
			while last_id != lesson.time:
				day.append({
					'title': '',
					'color': '',
					'intersect': '',
					'place': '',
				})
				last_id += 1

			color = 'olive'
			if lesson.type == 2: color = 'blue'
			elif lesson.type == 3: color = 'red'
			intersect = 'yellow' #пара свободна
			try: 
				our_lesson = Timetable.objects.get(semester = settings.SEMESTER, week = week, day = i, time = last_id)
				if lesson.lesson == our_lesson.lesson.title: intersect = 'teal' #пара у нас
				else: intersect = 'orange' #в данное время у нас пара
			except ObjectDoesNotExist:
				pass
			current = {
				'title': lesson.lesson, 
				'color': color,
				'intersect': intersect,
				'place': lesson.place,
				'group': lesson.group,
			}
			day.append(current)
			if lesson.double:
				day.append(current)
				last_id += 1
			last_id += 1
		while len(day) <= 7:
			last_id += 1
			day.append({
				'title': '',
				'color': '',
			})
		if week == 1: week1.append(day)
		elif week == 2: week2.append(day)

		i += 1		
		if i == 7 and week == 1: 			
			week = 2
			i = 1	
	context = {
		'week1': week1,
		'week2': week2,
		'title': teacher.name, 
		'bodyclass': 'profile-page',
		'name': teacher.name,
		'avatar': avatar,
		'teacher_id': teacher.id,
		'active_page': 2,
	}
	return render(request, 'teacher_timetable.html', context)