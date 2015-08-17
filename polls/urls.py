from django.conf.urls import url
from . import views

urlpatterns = [
	url('^$', views.index, name='index'),
	url('^add', views.add, name='add'),
	url('^(?P<id>[0-9]+)/$', views.poll, name='poll'),
	url('^close/(?P<id>[0-9]+)/$', views.close, name='close'),
	url('^open/(?P<id>[0-9]+)/$', views.open, name='open'),
	url('^comment/', views.poll_comment, name='poll_comment'),
	#url('^edit/(?P<id>[0-9]+)/$', views.edit, name='edit'),
	#url('^delete/(?P<id>[0-9]+)/$', views.delete, name='delete'),
]