from django.conf.urls import url
from . import views

urlpatterns = [
	url('^$', views.index, name='index'),
	#url('^?page=(?P<page>[0-9]+'), views.index, name='index'),
	url('^teacher/(?P<id>[0-9]+)', views.teacher, name='teacher'),
	url('^teacher/timetable/(?P<id>[0-9]+)', views.teacher_timetable, name='teacher_timetable'),
	url('^timetable/$', views.all_timetable, name='all_timetable'),
	url('^homework/add/', views.add_homework, name='add_homework'),
	url('^control/add/', views.add_control, name='add_control'),
	url('^change/place/', views.change_place, name='change_place'),
	url('^change/lesson/', views.transfer_lesson, name='transfer_lesson'),
	url('^change/cancel/', views.canceled_lesson, name='canceled_lesson'),
	url('^timetable/next_days/', views.timetableByDate, name='timetableByDate'),
]