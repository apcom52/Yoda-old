from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from achievements.models import Action, AchUnlocked
from django.db.models.fields import related
from django.core.exceptions import ObjectDoesNotExist 
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Lesson, Teacher, Timetable, Homework, Control, NewPlace, TeacherTimetable, NotStudyTime, TransferredLesson, CanceledLesson
from events.models import Event, UserVisitEvent
from notes.models import Note
from polls.models import Question
from .utils import DTControl, avatar, addAction, checkAchievements, setAch, dateInfo, getTimetable, UpdateStatus, getNotifications
from .forms import *
import datetime


# Create your views here.
def index(request):
	page = request.GET.get('page', 1)
	new_achievements = []
	if request.user.is_authenticated():
	#Получение списка новых достижений		
		UpdateStatus(request.user)
		checkAchievements(request.user)			
		try:
			my_new_ach = AchUnlocked.objects.all().filter(login = request.user).filter(is_new = True)
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
		pass
	
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
			changePlace = new_place.new_place
		except ObjectDoesNotExist:
			pass

		#Проверка на перенос пары
		is_transfered = False
		try:
			new_lesson_tr = TransferredLesson.objects.get(last_date = today_date, last_time = lesson.time)
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
	new_lesson_tr = TransferredLesson.objects.all().filter(new_date = timezone.now())
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
	canceled_lessons_list = CanceledLesson.objects.all().filter(date = timezone.now())
	print('===== %s' % (len(canceled_lessons_list),))
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

	print('!!!!! %s' % (len(canceled_lessons),))
	for tt in canceled_lessons:		
		for t in timetable:
			if t['num'] == tt['num']:
				t['is_canceled'] = True
				break			

	#Получение списка мероприятий
	start_event_date = timezone.now()
	end_event_date = start_event_date + datetime.timedelta(days=10)
	events_list = Event.objects.all().filter(date__gte = start_event_date).filter(date__lte = end_event_date).order_by('date')
	events = []
	for event in events_list:
		opinion = False
		if event.is_required == False:
			if request.user.is_authenticated():
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
	today_events = []
	if request.user.is_authenticated():
		time_now = timezone.now()
		end_time_now = time_now + datetime.timedelta(days = 1)
		my_canceled_events_list = UserVisitEvent.objects.all().filter(login = request.user, answer = 3)
		my_canceled_events = []
		for c in my_canceled_events_list: my_canceled_events.append(c.event.id)
		today_events_list = Event.objects.all().filter(date__gte = time_now).filter(date__lte = end_time_now).exclude(id__in = my_canceled_events)
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
		'notifications': getNotifications(request.user),
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
	if not request.user.is_authenticated(): return redirect('/auth/in')
	UpdateStatus(request.user)
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
	if not request.user.is_authenticated(): return redirect('/auth/in')
	UpdateStatus(request.user)
	weeks = []
	week1 = []
	week2 = []
	i = 1
	day = 1
	week = 1
	while i <= 6:
		lessons = Timetable.objects.all().filter(week = week, day = i, semester = settings.SEMESTER)
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
	if not request.user.is_authenticated(): return redirect('/auth/in')
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
				weeknumber = dt.isocalendar()[1]
				week = 1
				if (1 + weeknumber) % 2 == 0: week = 2
				lesson = Timetable.objects.get(semester = settings.SEMESTER, week = week, day = weekday, time = data['time'])
				addAction(request.user, 'добавил домашнее задание по предмету "' + lesson.lesson.title + '"')			
			except ObjectDoesNotExist:
				addAction(request.user, 'добавил домашнее задание')
			setAch(request.user, 6)
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
	if not request.user.is_authenticated(): return redirect('/auth/in')
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
				if (weeknumber) % 2 == 0: week = 2
				lesson = Timetable.objects.get(semester = settings.SEMESTER, week = week, day = weekday, time = data['time'])
				addAction(request.user, 'добавил информацию о контрольной по предмету "' + lesson.lesson.title + '" в базу')	
			except ObjectDoesNotExist:
					addAction(request.user, 'добавил информацию о контрольной в базу')	
			setAch(request.user, 6)
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
	if not request.user.is_authenticated(): return redirect('/auth/in')
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
				if (weeknumber) % 2 == 0: week = 2
				lesson = Timetable.objects.get(semester = settings.SEMESTER, week = week, day = weekday, time = data['time'])
				addAction(request.user, 'изменил аудиторию "%s (%s.%s.%s - %s пара)" на %s' % (lesson.lesson.title, set_date[2], set_date[1], set_date[0], data['time'], data['new_place']))	
			except ObjectDoesNotExist:
				addAction(request.user, 'добавил информацию о смене аудитории')	
			setAch(request.user, 6)
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
	if not request.user.is_authenticated(): return redirect('/auth/in')
	UpdateStatus(request.user)
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
		lessons = TeacherTimetable.objects.all().filter(teacher = teacher, week = week, day = i, semester = settings.SEMESTER)
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

def transfer_lesson(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	error = [False, '']
	form = ChangeLessonForm()	
	if request.method == 'POST':
		data = request.POST
		form = ChangeLessonForm(data)
		if form.is_valid() and data['new_place']:
			try:
				has_changing = TransferredLesson.objects.get(last_date = data['last_date'], last_time = data['last_time'], new_date = data['new_date'], new_time = data['new_time'])
			except ObjectDoesNotExist:				
				newlesson = TransferredLesson()
				try: 
					set_date = data['last_date'].split('-')
					dt = datetime.date(int(set_date[0]), int(set_date[1]), int(set_date[2]))
					weekday = dt.isoweekday()
					weeknumber = int(dt.strftime('%U'))
					week = 1
					if (weeknumber) % 2 == 0: week = 2
					lesson = Timetable.objects.get(semester = settings.SEMESTER, week = week, day = weekday, time = data['last_time'])
				except ObjectDoesNotExist:
					raise ObjectDoesNotExist
				newlesson.login = request.user
				newlesson.lesson = lesson
				newlesson.last_date = data['last_date']
				newlesson.last_time = data['last_time']
				newlesson.new_date = data['new_date']		
				newlesson.new_time = data['new_time']	
				newlesson.new_place = data['new_place']	
				newlesson.save()	
			addAction(request.user, 'добавил информацию о переносе пары')	
			setAch(request.user, 6)
			
			return redirect('/')
		else:
			error[0] = True
			error[1] = 'Произошла ошибка при переносе пары'
	context = {
		'title': 'Перенести пару',
		'form': form,
		'error': error[0],
		'error_message': error[1],
	}
	return render(request, 'transfer_lesson.html', context)

def canceled_lesson(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	error = [False, '']
	form = CanceledLessonForm()	
	if request.method == 'POST':
		data = request.POST
		form = CanceledLessonForm(data)
		if form.is_valid():
			try:
				has_changing = CanceledLesson.objects.get(date = data['date'], time = data['time'])
			except ObjectDoesNotExist:				
				newlesson = CanceledLesson()
				newlesson.login = request.user
				newlesson.date = data['date']
				newlesson.time = data['time']
				newlesson.save()	
			addAction(request.user, 'добавил информацию об отмене пары')	
			setAch(request.user, 6)
			
			return redirect('/')
		else:
			error[0] = True
			error[1] = 'Произошла ошибка при отмене пары'
	context = {
		'title': 'Отменить пару',
		'form': form,
		'error': error[0],
		'error_message': error[1],
	}
	return render(request, 'cancel_lesson.html', context)

def timetableByDate(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	UpdateStatus(request.user)
	today = timezone.localtime(timezone.now())
	tomorrow = today + datetime.timedelta(days = 1)
	second = today + datetime.timedelta(days = 2)
	third = today + datetime.timedelta(days = 3)
	tomorrow_info = dateInfo({'year': tomorrow.year, 'month': tomorrow.month, 'day': tomorrow.day})
	second_info = dateInfo({'year': second.year, 'month': second.month, 'day': second.day})
	third_info = dateInfo({'year': third.year, 'month': third.month, 'day': third.day})	
	first = getTimetable(week = tomorrow_info['week'], day = tomorrow_info['weekday'], date = tomorrow)
	second = getTimetable(week = second_info['week'], day = second_info['weekday'], date = second)
	third = getTimetable(week = third_info['week'], day = third_info['weekday'], date = third)
	context = {
		'first': first,
		'second': second,
		'third': third,
	}
	return render(request, 'tomorrow_timetable.html', context)

def teacher_index(request):
	UpdateStatus(request.user)
	teachers_list = Teacher.objects.all().filter(semester = settings.SEMESTER)
	teachers = []
	for teacher in teachers_list:
		teachers.append({
			'name': teacher.name,
			'id': teacher.id,
			'image': teacher.avatar.url,
		})
	context = {
		'title': 'Преподаватели',
		'teachers': teachers,
	}
	return render(request, 'teachers_index.html', context)

def beta_index(request):
	#Получение расписания
	today = getTimeTable(3, 2, 1)
	#Получение списка активности
	page = request.GET.get('page', 1)
	actions_list = Action.objects.all().order_by('-pub_date')
	p = Paginator(actions_list, 25)
	if int(page) < 1: page = 1
	elif int(page) > p.num_pages: page = p.num_pages
	current_page = p.page(page)
	actions = []
	for action in current_page.object_list:	
		actions.append({
			'username': action.login.get_full_name(),
			'avatar': avatar(action.login),
			'text': action.text,
			'pub_date': action.pub_date,
		})

	last_week = datetime.datetime.today() - datetime.timedelta(days=7)
	#Получение последних заметок
	lates_notes = Note.objects.all().filter(pub_date__gte = last_week).order_by('-pub_date')
	notes = []
	for note in lates_notes:
		notes.append({
			'id': note.id,
			'title': note.title,
		})
	#Получение последних заметок
	lates_polls = Question.objects.all().filter(pub_date__gte = last_week).order_by('-pub_date')
	polls = []
	for poll in lates_polls:
		polls.append({
			'id': poll.id,
			'title': poll.title,
		})

	context = {
		'title': 'Главная - Yoda',
		'timetable': today,
		'actions': actions,
		'notes': notes,
		'polls': polls,
		'pagination': {
				'has_prev': current_page.has_previous(),
				'has_next': current_page.has_next(),
				'current': current_page.number,
				'prev': current_page.number - 1,
				'next': current_page.number + 1,
			},
	}
	return render(request, 'beta/index.html', context)

def getTimeTable(semester, week, day, date = datetime.datetime.now()):
	timetable = []
	today = DTControl()	
	timetable_list = Timetable.objects.all().filter(semester = semester, week = week, day = day)
	for lesson in timetable_list:
		type_color = 'olive'
		type_name = 'Лекция'
		if lesson.lesson.type == 2:
			type_color = 'blue'
			type_name = 'Практика'
		elif lesson.lesson.type == 3:
			type_color = 'red'
			type_name = 'Лабораторная работа'
		timetable.append({
			'title': lesson.lesson.title,
			'teacher': lesson.teacher.name,
			'time': today.getTimeFromNum(lesson.time),
			'type': {
				'type': lesson.lesson.type,
				'color': type_color,
				'name': type_name,
			},
			'place': lesson.place,			
		})
	return timetable