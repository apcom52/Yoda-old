import datetime
from django.db.models import Q
from rest_framework import serializers
from .models import *

class TimetableSerializer(serializers.ModelSerializer):
	title = serializers.CharField(source = 'lesson.title', allow_blank = True)
	time = serializers.SerializerMethodField()
	teacher = serializers.CharField(source = 'teacher.name', allow_blank = True)
	type_css = serializers.SerializerMethodField()
	type = serializers.SerializerMethodField()

	def get_time(self, obj):
		times = ['8:20','10:00','11:45','14:00','15:45','17:20','18:55']
		return times[obj.time - 1]

	def get_type_css(self, obj):
		types = ['lection', 'practice', 'lab']
		return types[obj.lesson.type - 1]

	def get_type(self, obj):
		types = ['Лекция', 'Практика', 'Лабораторная работа']
		return types[obj.lesson.type - 1]

	class Meta:
		model = Timetable
		fields = (
			'title', 'time', 'place', 'teacher', 'type', 'type_css'
		)

class TimetableWeekSerializer():
	date = None
	timetable = None

	def __init__(self, date, group, semester):
		data_day = date
		dt = datetime.datetime.strptime(data_day, '%d/%m/%Y')
		self.start = dt - datetime.timedelta(days=dt.weekday())
		self.end = self.start + datetime.timedelta(days=6)
		self.week_num = self.start.day#self.start.isocalendar()[1]
		self.week_type = 1
		if self.week_num % 2 == 0: 
			self.week_type = 2
		self.group = group
		self.semester = semester

	def get_data(self):
		self.timetable = []
		for i in range(1, 8):
			tt = Timetable.objects.all().filter(semester = self.semester, week = self.week_type, day = i).filter(Q(group = 1) | Q(group = (self.group + 1))).order_by('time')
			serializer = TimetableSerializer(tt, many = True)
			current_date = datetime.datetime.date(self.start + datetime.timedelta(days = i-1))
			date = datetime.datetime.strftime(self.start + datetime.timedelta(days = i-1), "%d %B")
			today = False
			
			if current_date.day == datetime.datetime.today().day and current_date.month == datetime.datetime.today().month:
				today = True
			is_weekend = False
			if len(tt) < 1: 
				is_weekend = True

			self.timetable.append({
				'timetable': serializer.data,
				'date': date,
				'weekend': is_weekend,
				'today': today,
				})

		return self.timetable