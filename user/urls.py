from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
	url('^(?P<id>[0-9]+)/', views.profile, name='profile'),	
	url('^achievements/(?P<id>[0-9]+)', views.achievements, name='achievements'),
	url('^content/(?P<id>[0-9]+)', views.user_content, name='user_content'),
	url('^attendance/(?P<id>[0-9]+)', views.my_attendance, name='my_attendance'),
	url('^duty/(?P<id>[0-9]+)', views.my_duties, name='my_duties'),
	url('^inventory/(?P<id>[0-9]+)', views.inventory, name='inventory'),
	url('^collection/(?P<id>[0-9]+)', views.collection, name='collection'),
	url('^stats/(?P<id>[0-9]+)', views.statistic, name='statistic'),
	url('^settings/', views.user_settings, name='settings'),
	url('^lottery/', views.lottery, name='lottery'),
	url('^complect/', views.complect, name='complect'),
	url('^upload_photo/', views.upload_photo, name='upload_photo'),
	url('^change_password/', views.change_password, name='change_password'),
	url('^set_contacts/', views.set_contacts, name='set_contacts'),
	#url('^send_notification/', views.addNotification, name='addNotification'),
	url('^duty_done/', views.duty_done, name='duty_done'),
	url('^save_additional/', views.save_additional, name='save_additional'),
	url('^sold/', views.sold_inventory_item, name='sold_inventory_item'),
	url('^send_catapult/', views.send_catapult, name='send_catapult'),
	url('^open_case/(?P<id>[0-9]+)/', views.open_case, name='open_case'),
]