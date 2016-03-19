from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
	url(r'^up', views.signup, name='signup'),
	url(r'^in', views.signin, name='signin'),
	url(r'^out', views.signout, name='signout'),	
	url(r'^premier', views.premier, name='premier'),	
	url(r'^game', views.game, name='game'),	
]