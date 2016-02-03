from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from library.serializers import *
from user.serializers import *
from notes.serializers import *
from favorites.serializers import *

from library.models import *
from notes.models import Note

# Create your views here.
class LibraryFilesAPI(APIView):	
	def get(self, request, format = None):
		#file, serializer = None
		data = request.GET
		
		if data.get("id"):
			file = LibraryFile.objects.get(pk = int(data.get("id")))
			file.views += 1
			file.save()

			tags = file.tags.all()
			for tag in tags:
				tag.views += 1
				tag.save()
			serializer = LibraryFileSerializer(file, many = False)

		elif data.get("q"):
			query = (data.get('q')).lower()
			file = LibraryFile.objects.all().filter(Q(title__icontains = query.capitalize()) | Q(description__icontains = query.capitalize()) | Q(title__icontains = query.upper()) | Q(description__icontains = query.upper()) | Q(title__icontains = query.lower()) | Q(description__icontains = query.lower())).order_by('-id').distinct()	
			serializer = LibraryFileSerializer(file, many = True, read_only = True)

		else:
			file = LibraryFile.objects.all().order_by('-id')
			serializer = LibraryFileSerializer(file, many = True)
		return Response(serializer.data)

	def post(self, request, format = None):
		print(self.request)
		login = request.user
		print(request.data)
		file = request.data['file']
		title = request.data['title']
		description = request.data['description']

		libraryFile = LibraryFile()
		libraryFile.title = title
		libraryFile.description = description
		libraryFile.file = file
		libraryFile.login = login
		libraryFile.save()
		data = LibraryFileSerializer(libraryFile)
		return Response(data.data)


class LibraryTagAPI(APIView):
	def get(self, request, format = None):
		data = request.GET
		if (data.get("count")):
			tags = LibraryTag.objects.all().order_by('-views')[:int(data.get("count"))]						
		else:
			tags = LibraryTag.objects.all().order_by('-views')
		serializer = LibraryTagSerializer(tags, many = True)
		return Response(serializer.data)

class UserAPI(APIView):
	def get(self, request, format = None):
		data = request.GET
		if (data.get("id")):
			users = User.objects.filter(id__exact = int(data.get('id')))
		else:
			users = User.objects.all()
		serializer = UserSerializer(users, many = True)
		return Response(serializer.data)


class AttendanceAPI(APIView):
	def get(self, request, format = None):
		data = request.GET
		attendances = Attendance.objects.all()
		serializer = AttendanceSerializer(attendances, many = True)
		return Response(serializer.data)

@csrf_exempt
@api_view(['GET', 'POST', 'PUT'])
def library_tag_category(self, request):
	if request.method == 'GET':
		files = LibraryTagCategory.objects.all()
		serializer = LibraryTagCategorySerializer(files, many = True)
		return Response(serializer.data)
	elif request.method == 'POST' or request.method == 'PUT':
		serializer = LibraryTagCategorySerializer(data = request.data)
		print(request.data)
		if serializer.is_valid():
			serializer.save()
			print("true valid")
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



		org = Organization.objects.all()
		serializer = OrganizationsSerializer(org, many = True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = OrganizationsSerializer(data = request.DATA)
		if 	serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class NoteAPI(APIView):	
	def get(self, request, format = None):
		#file, serializer = None
		data = request.GET
		
		if data.get("id"):
			note = Note.objects.get(pk = int(data.get("id")))
			note.views += 1
			note.save()

			serializer = NoteSerializer(note, many = False, context = { 'request': request})		
		else:
			note = Note.objects.all().order_by('-id')
			serializer = NoteSerializer(note, many = True, context = { 'request': request})
		return Response(serializer.data)
	def post(self, request, format = None):
		data = request.data

		note = Note()
		if data['title'] and data['content']:			
			note.title = data['title']
			note.content = data['content']
			note.pub_date = timezone.now() + timezone.timedelta(hours=3)
			note.login = request.user
			note.save()

		serializer = NoteSerializer(note, many = False, context = { 'request': request})
		return Response(serializer.data)
	def put(self, request, format = None):
		data = request.data
		print('==== PUT ======')
		print(data)
		note = Note()
		serializer = NoteSerializer(note, many = False, context = { 'request': request})
		try:
			note = Note.objects.get(pk = data['id'])
			note.views = data['views']
			note.save()
			serializer = NoteSerializer(note, many = False, context = { 'request': request})
			return Response(serializer.data)
		except ObjectDoesNotExist:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class FavoriteAPI(APIView):
	def get(self, request, format = None):
		favorites = Favorite.objects.all().order_by('-id')
		serializer = FavoriteSerializer(favorites, many = True, context = { 'request': request})
		return Response(serializer.data)
	def post(self, request, format = None):
		data = request.data
		print('=====', data)
		login = request.user
		type = data['type']
		note = Note.objects.get(pk = data['note'])

		try:
			favorite = Favorite.objects.get(login = login, type = type, note = note)
			favorite.delete()
		except ObjectDoesNotExist:
			favorite = Favorite()
			favorite.login = login
			favorite.type = type
			favorite.note = note
			favorite.save()
		serializer = FavoriteSerializer(favorite, context = { 'request': request})
		return Response(serializer.data)

class SettingsAPI(APIView):
	def post(self, request, format = None):
		user = request.user
		user.userprofile.accent = 'blue'
		user.save()
		return Response()


		'''user = request.user
		data = request.POST
		print(data)
		method = data.get('m', False)
		print(method)
		
		if method == 'accent':
			print('change accent')			
			user.userprofile.accent = data['accent']
			user.save()
		elif method == 'theme':
			print('change theme')			
			user.userprofile.theme = data['theme']
			user.save()		
		
		serializer = UserSerializer(user, many = False)
		print(user.userprofile.accent)
		return Response(serializer.data)'''

		'''serializer = UserSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
		return Response(serializer.data)'''