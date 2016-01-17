from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from timetable.utils import pointsumm, getrank, isOnline

class UserSerializer(serializers.ModelSerializer):
	facebook = serializers.CharField(source = 'userprofile.facebook', allow_blank = True)
	vk = serializers.CharField(source = 'userprofile.vk', allow_blank = True)
	twitter = serializers.CharField(source = 'userprofile.twitter', allow_blank = True)
	phone = serializers.CharField(source = 'userprofile.phone', allow_blank = True)
	avatar = serializers.ImageField(source = 'userprofile.avatar', allow_empty_file = True)
	last_visit = serializers.DateTimeField(source = 'userprofile.last_visit')
	theme = serializers.CharField(source = 'userprofile.theme', allow_blank = True)
	accent = serializers.CharField(source = 'userprofile.accent', allow_blank = True)
	points = serializers.SerializerMethodField()
	rank = serializers.SerializerMethodField()
	is_online = serializers.SerializerMethodField()

	def get_points(self, obj):
		return pointsumm(obj)

	def get_rank(self, obj):
		return getrank(obj)

	def get_is_online(self, obj):
		return isOnline(obj)

	class Meta:
		model = User
		fields = (
			'id',	'username',	'first_name','last_name',	'email',
			'is_active', 'facebook', 'vk', 'twitter', 'phone', 'avatar', 
			'last_visit',	'points',	'rank',	'is_online', 'theme',
			'accent',
		)

class AttendanceSerializer(serializers.ModelSerializer):
	type_value = serializers.SerializerMethodField()

	def get_type_value(self, obj):
		if obj.type == 1: return 'Лекция'
		elif obj.type == 2:	return 'Практика'
		return 'Лабораторная работа'

	class Meta:
		model = Attendance
		fields = (
			'lesson',	'date',		'type_value',		'visitor',
		)
