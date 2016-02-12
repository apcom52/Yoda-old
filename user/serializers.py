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
class SettingsSerializer(serializers.ModelSerializer):
	facebook = serializers.CharField(required = False, allow_blank = True)
	vk = serializers.CharField(required = False, allow_blank = True)
	twitter = serializers.CharField(required = False, allow_blank = True)
	github = serializers.CharField(required = False, allow_blank = True)
	phone = serializers.CharField(required = False, allow_blank = True)
	beta = serializers.CharField(required = False, allow_blank = True)
	
	avatar = serializers.ImageField(required = False, allow_empty_file = True)

	theme = serializers.CharField(required = False, allow_blank = True)
	accent = serializers.CharField(required = False, allow_blank = True)
	
	hide_email = serializers.CharField(required = False, allow_blank = True)
	hide_tips = serializers.CharField(required = False, allow_blank = True)
	
	filter_achievements = serializers.CharField(required = False, allow_blank = True)
	filter_sales = serializers.CharField(required = False, allow_blank = True)
	filter_catapult = serializers.CharField(required = False, allow_blank = True)
	filter_bonuses = serializers.CharField(required = False, allow_blank = True)

	notes_night_mode = serializers.CharField(required = False, allow_blank = True)
	notes_font_size = serializers.CharField(required = False, allow_blank = True)
	notes_font_style = serializers.CharField(required = False, allow_blank = True)

	polls_actual = serializers.CharField(required = False, allow_blank = True)

	events_notification = serializers.CharField(required = False, allow_blank = True)
	events_time_notification = serializers.CharField(required = False, allow_blank = True)
	

	class Meta:
		model = UserProfile
		fields = ('facebook', 'vk', 'twitter', 'github',
			'phone', 'avatar', 'theme', 'accent', 'beta', 'hide_email', 'hide_tips',
			'filter_achievements', 'filter_sales', 'filter_catapult',
			'filter_bonuses', 'notes_night_mode', 'notes_font_size',
			'notes_font_style', 'polls_actual', 'events_notification', 
			'events_time_notification')

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
