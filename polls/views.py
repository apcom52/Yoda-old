from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError 
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from timetable.utils import addAction, avatar, setAch
from .models import *
from .forms import AddPollForm
from .utils import changePollState

# Create your views here.
def index(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	polls = Question.objects.order_by('-pub_date').all()
	context = {'title':'Опросы', 'polls':polls}
	return render(request, 'polls_index.html', context)

def add(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	error = [False, '']
	form = AddPollForm()	
	if request.method == 'POST':
		data = request.POST
		form = AddPollForm(data)
		options = data['options'].split('\n')		
		if form.is_valid() and len(options) >= 2:
			poll = Question()
			poll.login = request.user
			poll.title = data['title']
			poll.type = data['type']
			poll.pub_date = timezone.now()
			if 'is_anon' in data:
				poll.is_anon = True
			else:
				poll.is_anon = False
			poll.is_closed = False
			poll.save()
			for opt in options:
				answer = Answer()
				answer.text = opt
				answer.save()
				poll.choices.add(answer)			
			addAction(request.user, 'добавил опрос <a href="/polls/%s/">%s</a>' % (poll.id, poll.title))	
			setAch(request.user, 3)		
			return redirect('/polls/')
		else:
			error_message = 'Проверьте правильность введенных данных. Количество вариантов ответа должно быть не менее двух'			
			error[0] = True
			error[1] = error_message
	context = {
		'title': 'Добавить опрос',
		'form': form,		
		'error': error[0],
		'error_message': error[1],
	}
	return render(request, 'add_poll.html', context)

@csrf_exempt
def poll(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		poll = Question.objects.get(id = id)
		voted_count = len(QueAns.objects.all().filter(question = poll))
		you_voted = False
		if poll.login == request.user or request.user.is_superuser:
			is_author = True
		else: is_author = False
		votes = []

		comments = []
		comments_list = PollComment.objects.all().filter(poll = poll)
		for comment in comments_list:
			comments.append({
				'username': '%s %s' %(comment.login.first_name, comment.login.last_name),
				'avatar': avatar(comment.login),
				'text': comment.comment,
				'date': comment.pub_date,
				'user_id': comment.login.id,
			})

		if QueAns.objects.filter(login = request.user, question = poll) or poll.is_closed:
			you_voted = True		
			for choice in poll.choices.all():
				voters = []					
				for us in QueAns.objects.all().filter(answer = choice.id):
					user = us.login					
					current = {
						'user': user,
						'avatar': avatar(user),
					}
					voters.append(current)
				opt = {
					'text': choice.text,
					'users': voters,
				}
				votes.append(opt)
		else:				
			if request.method == 'POST':
				data = request.POST				
				for opt in data.getlist('options'):				
					choice = QueAns()
					choice.login = request.user
					choice.question = poll
					choice.answer = int(opt)
					choice.save()					
				return redirect('/polls/' + str(poll.id))
		context = {
			'title': poll.title,
			'poll': poll,
			'is_author': is_author,
			'avatar': avatar(poll.login),
			'voted_count': voted_count,
			'you_voted': you_voted,
			'votes': votes,
			'comments': comments,
			'comment_url': '/polls/comment/',
			'comment_item_id': poll.id,
		}
		return render(request, 'poll.html', context)
	except ObjectDoesNotExist:		
		return redirect('/polls/')

def close(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if changePollState(request, id, 'close'):
		return redirect('/polls/' + id)
	else:
		return redirect('/polls/')

def open(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if changePollState(request, id, 'open'):
		return redirect('/polls/' + id)
	else:
		return redirect('/polls/')

def poll_comment(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if request.method == 'POST':
		data = request.POST
		poll_id = data['item_id']
		try:
			poll = Question.objects.get(id = poll_id)
			user = request.user
			text = data['comment']
			if len(text) >= 1:
				comment = PollComment()
				comment.login = user
				comment.poll = poll
				comment.comment = text
				comment.pub_date = timezone.now()
				comment.save()		
				addAction(user, 'добавил комментарий в опросе <a href="/polls/%s">%s</a>' % (poll.id, poll.title))
		except ObjectDoesNotExist:
			pass	
	return redirect('/polls/%s/' % (poll_id,))