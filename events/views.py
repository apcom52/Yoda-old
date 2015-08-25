from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from achievements.models import Action
from timetable.utils import addAction, setAch, avatar
from .forms import *
from .models import *
import pymorphy2

# Create your views here.
def index(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	events_list = Event.objects.all().filter(date__gte = timezone.now()).order_by('date')
	events = []
	for event in events_list:
		answer = ""
		answer_color = ""
		if event.is_required == False:
			try: 
				my_answer = UserVisitEvent.objects.get(event = event.id, login = request.user)
				if my_answer.answer == 1:
					answer = "Пойду"
					answer_color = "green"
				elif my_answer.answer == 2:
					answer = "Возможно пойду"
					answer_color = "yellow"
				elif my_answer.answer == 3:
					answer = "Не пойду"
					answer_color = "orange"
			except ObjectDoesNotExist:
				answer = "Вы не дали ответа"
				answer_color = ""
		events.append({
			'event': event,
			'answer': answer,
			'answer_color': answer_color,
		})
	context = {'title':'Мероприятия', 'events':events}
	return render(request, 'events_index.html', context)

def add(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	error = [False, '']
	form = EventAddForm()
	if request.method == 'POST':
		data = request.POST
		form = EventAddForm(data)
		if form.is_valid() and len(data['title']) >= 2 and len(data['date']) >= 10:
			event = Event()
			event.title = data['title']
			event.description = data['description']
			event.date = data['date']
			event.login = request.user
			if 'is_required' in data:
				event.is_required = True
			else:
				event.is_required = False
			event.save()
			#Добавление действия в базу
			addAction(request.user, 'добавил мероприятие <a href="/events/%s">%s</a>' % (event.id, data['title']))
			setAch(request.user, 14)
			return redirect('/')
		else:
			error_message = 'Произошла ошибка'
			if len(data['title'])< 2 or len(data['date']) < 10: error_message = 'Введите правильное название мероприятия и дату'	
			error[0] = True
			error[1] = error_message
	context = {'title': 'Мероприятия', 'form': form, 'error':error[0], 'error_text': error[1]}
	return render(request, 'event_add.html', context)

def event(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		event = Event.objects.get(id = id)	
		visit = []
		not_sure = []
		no_visit = []
		your_answer = 0
		try:
			visiters = UserVisitEvent.objects.all().filter(event = event)
			for visiter in visiters:
				current = {
					'username': '%s %s' % (visiter.login.first_name, visiter.login.last_name),
					'user_id': visiter.login.id,
					'avatar': avatar(visiter.login),
				}
				if visiter.login == request.user:
					your_answer = visiter.answer
				if visiter.answer == 1:
					visit.append(current)
				elif visiter.answer == 2:
					not_sure.append(current)
				elif visiter.answer == 3:
					no_visit.append(current)
		except ObjectDoesNotExist:
			pass

		comments = []
		comments_list = EventComment.objects.all().filter(event = event)
		for comment in comments_list:
			comments.append({
				'username': '%s %s' %(comment.login.first_name, comment.login.last_name),
				'avatar': avatar(comment.login),
				'text': comment.comment,
				'date': comment.pub_date,
				'user_id': comment.login.id,
			})

		context = {
			'event': event,
			'visit': visit,
			'not_sure': not_sure,
			'no_visit': no_visit,
			'your_answer': your_answer,
			'author': event.login,
			'author_username': '%s %s' % (event.login.first_name, event.login.last_name),
			'author_avatar': avatar(event.login),
			'comments': comments,
			'comment_url': '/events/comment/',
			'comment_item_id': event.id,
		}
		return render(request, 'event.html', context)
	except ObjectDoesNotExist:		
		return redirect('/polls/')

@csrf_exempt
def answer(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if request.GET:
		data = request.GET		
		event_id = data.get('id', 0)
		answer = data.get('answer', 0)
		if event_id and answer:
			try:
				my_answer = UserVisitEvent.objects.get(event = event_id, login = request.user)
				my_answer.answer = answer
				my_answer.save()
			except ObjectDoesNotExist:
				event = Event.objects.get(id = event_id)
				my_answer = UserVisitEvent()
				my_answer.event = event
				my_answer.login = request.user
				my_answer.answer = answer
				my_answer.save()
			return redirect('/events/%s' % (event_id,))
	return redirect('/events/')

def event_comment(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if request.method == 'POST':
		data = request.POST
		event_id = data['item_id']
		try:
			event = Event.objects.get(id = int(event_id))
			user = request.user
			text = data['comment']
			if len(text) >= 1:
				comment = EventComment()
				comment.login = user
				comment.event = event
				comment.comment = text
				comment.pub_date = timezone.now()
				comment.save()		
				addAction(user, 'добавил комментарий о мероприятии <a href="/events/%s">%s</a>' % (event.id, event.title))
		except ObjectDoesNotExist:
			pass	
	return redirect('/events/%s/' % (event_id,))