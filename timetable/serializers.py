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

class TimetableWeekSerializer(serializers.ModelSerializer):
	day = serializers.SerializerMethodField()
	month = serializers.SerializerMethodField()
	is_weekend = serializers.SerializerMethodField()
	timetable = TimetableSerializer(many = True)

	def get_day(self, obj):
		import datetime
		today = datetime.datetime.today()
		d = "" + today.year() + "-W" + self.context.get('weekday')
		r = datetime.datetime.strptime(d + '-0', "%Y-W%W-%w")
		return r.day
	
