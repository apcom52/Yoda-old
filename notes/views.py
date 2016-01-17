from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from achievements.models import Action
from timetable.utils import addAction, avatar, setAch, UpdateStatus, bingo, setBonusPoints
#from user.utils import getSmiles
from .forms import NoteAddForm, NoteEditForm
from .models import *

import bbcode

# Create your views here.
def index(request):	
	if not request.user.is_authenticated(): return redirect('/auth/in')
	bonus = setBonusPoints(request.user)	
	white = request.GET.get('white', False)
	_bingo = bingo(request.user)
	UpdateStatus(request.user)
	notes = Note.objects.order_by('-pub_date').all()
	context = {'title': 'Заметки', 'notes':notes, 'bingo': _bingo, 'bonus': bonus, 'white': white,}
	if request.user.userprofile.beta:	return render(request, 'beta/notes_index.html', context)
	else:	return render(request, 'notes_index.html', context)

def add(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	UpdateStatus(request.user)
	error = [False, '']
	form = NoteAddForm()
	white = request.GET.get('white', False)
	if request.method == 'POST':
		data = request.POST
		form = NoteAddForm(data)
		title = data['title']
		content = data['content']
		if form.is_valid() and len(content) >= 10 and len(title) >= 2:
			note = Note()
			note.title = title
			note.content = content
			note.login = request.user
			note.pub_date = timezone.now()
			note.save()
			# добавление действия в таблицу
			addAction(request.user, 'добавил заметку <a href="/notes/%s/">"%s"</a>' % (note.id, note.title))
			setAch(request.user, 2)
			return redirect('/notes/')
		else:
			error_message = 'Произошла ошибка'
			if len(content)	< 10 or len(title) < 2: error_message = 'Заголовок должен быть не менее 2 символов. Содержание заметки не менее 10-ти символов'	
			error[0] = True
			error[1] = error_message
	context = {'title': 'Заметки', 'form':form, 'error':error[0], 'error_text': error[1], 'white': white,}
	if request.user.userprofile.beta:	return render(request, 'beta/note_add.html', context)
	return render(request, 'notes_add.html', context)

def note(request, id):	
	if not request.user.is_authenticated(): return redirect('/auth/in')
	try:
		bonus = setBonusPoints(request.user)	
		_bingo = bingo(request.user)
		UpdateStatus(request.user)
		context = {}	
		note = Note.objects.get(id = id)
		note.views += 1
		note.save()
		us = note.login		
		user_is_author = False
		white = request.GET.get('white', False)
		try:
			if request.user.username == us.username or request.user.is_admin: user_is_author = True
		except AttributeError:
			pass		
		username = us.first_name + ' ' + us.last_name

		comments = []
		comments_list = NoteComment.objects.all().filter(note = note)
		for comment in comments_list:
			comment_text = comment.comment#parseSmiles(comment.comment)
			comments.append({
				'username': '%s %s' %(comment.login.first_name, comment.login.last_name),
				'avatar': avatar(comment.login),
				'text': comment_text,
				'date': comment.pub_date,
				'user_id': comment.login.id,
			})

		notes = Note.objects.order_by('-pub_date').all()
		#Подгатавливаем контент
		content = wiki2html(note.content)
		context = {
			'title': note.title,
			'content': content,
			'login': us.id,
			'pub_date': note.pub_date,
			'views': note.views,
			'user_is_author': user_is_author,
			'username': username,
			'id': note.id,
			'user': us,
			'note': note,
			'comments': comments,
			'comment_url': '/notes/comment/',
			'comment_item_id': note.id,
			'bingo': _bingo,
			'bonus': bonus,
			'notes': notes,
			'white': white,
			#'smiles': getSmiles(request.user),
		}
		if request.user.userprofile.beta:	return render(request, 'beta/note.html', context)
		else:	return render(request, 'note.html', context)
	except ObjectDoesNotExist: 
		return redirect('/notes/')	

def edit(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if request.method == 'POST':
		try:
			data = request.POST
			note = Note.objects.get(id = id)
			note.title = data['title']
			note.content = data['content']
			note.save()
			return redirect('/notes/' + str(note.id) + '/')
		except ObjectDoesNotExist:
			return redirect('/notes/')
	else:
		try:		
			note = Note.objects.get(id = id)
			form = NoteEditForm()
			context = {'id': note.id, 'title': note.title, 'form': form}
			form.fields["title"].initial = note.title
			form.fields["content"].initial = note.content
			context = {'id': note.id, 'title': note.title, 'form': form}
			if (request.user == note.login or user.is_admin):				
				return render(request, 'notes_edit.html', context)
			else:
				raise ObjectDoesNotExist
		except ObjectDoesNotExist:
			return redirect('/notes/')

@csrf_exempt
def delete(request, id):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if request.method == 'POST' and request.POST['delete'] == 'True':
		try:		
			note = Note.objects.get(id = id)		
			if (str(request.user) == note.login or request.user.is_superuser): 
				note.delete()
				return redirect('/notes/')
			else:
				raise ObjectDoesNotExist
		except ObjectDoesNotExist:
			return redirect('/notes/')
	else:
		try:		
			note = Note.objects.get(id = id)	
			context = {'id': note.id, 'title': note.title}	
			if (str(request.user) == note.login or request.user.is_superuser): 
				return render(request, 'notes_delete.html', context)
			else:
				raise ObjectDoesNotExist
		except ObjectDoesNotExist:
			return redirect('/notes/')

def note_comment(request):
	if not request.user.is_authenticated(): return redirect('/auth/in')
	if request.method == 'POST':
		data = request.POST
		note_id = data['item_id']
		try:
			note = Note.objects.get(id = int(note_id))
			user = request.user
			text = data['comment']
			text = text.strip()
			if len(text) >= 1:
				comment = NoteComment()
				comment.login = user
				comment.note = note
				comment.comment = text
				comment.pub_date = timezone.now()
				comment.save()		
				addAction(user, 'добавил комментарий в заметке <a href="/notes/%s">%s</a>' % (note.id, note.title))
		except ObjectDoesNotExist:
			pass	
	return redirect('/notes/%s/' % (note_id,))

#Функция преобразования вики-тегов в html
'''def html_escape(char):
	if char == '&': return '&amp;'
	elif char == '"': return '&quot;'
	elif char == "'": return '&apos;'
	elif char == '>': return '&gt;'
	elif char == '<': return '&lt;'
	else: return char'''

def wiki2html(data = ''):
	'''html_escape_table = {
		'&': '&amp;',
		'"': '&quot;',
		"'": '&apos;',
		'>', '&gt',
		'<', '&lt',
	}'''
	#data = data.replace('[', '<')
	#data = data.replace(']', '>')
	#p = re.compile('\[{1}(/?\w*{1})[\]]')
	#result = re.sub('\[(/?\w*[^\])]+)', '<\1\0\2>', data.rstrip().lstrip())
	parser = bbcode.Parser()
	parser.add_simple_formatter('h', '<h2 name="%(value)s">%(value)s</h2>')
	parser.add_simple_formatter('h2', '<h3>%(value)s</h3>')
	#parser.add_simple_formatter('img', '<img src="%(value)s">')	
	result = parser.format(data)
	#result = result.replace('{{', '[')
	#result = result.replace('}}', ']')
	#result = bbcode.render_html(data)
	'''result = result.replace('>', '&gt')
	result = result.replace('<', '&lt')	
	result = result.replace('[h2]', '[h3]'); result = result.replace('[/h2]', '[/h3]');
	result = result.replace('[h]', '[h2]'); result = result.replace('[/h]', '[/h2]');
	result = result.replace('[', '<')
	result = result.replace(']', '>')
	result = result.replace('{{', '[')
	result = result.replace('}}', ']')'''
	#result = re.sub('\[{1}(/?\w*)[\]]', '\1\0\2', data)#p.sub('<\1>', data)
	return result