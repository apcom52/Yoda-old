from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
	url('^(?P<id>[0-9]+)/', views.profile, name='profile'),	
	url('^achievements/(?P<id>[0-9]+)', views.achievements, name='achievements'),
	url('^content/(?P<id>[0-9]+)', views.user_content, name='user_content'),
	url('^settings/', views.settings, name='settings'),
	url('^upload_photo/', views.upload_photo, name='upload_photo'),
	url('^change_password/', views.change_password, name='change_password'),
	url('^set_contacts/', views.set_contacts, name='set_contacts'),
	#url('^settings/' views.settings, name='settings'),
]