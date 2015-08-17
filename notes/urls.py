from django.conf.urls import url
from . import views

urlpatterns = [
	url('^$', views.index, name='index'),
	url('^add', views.add, name='add'),
	url('^(?P<id>[0-9]+)/$', views.note, name='note'),
	url('^edit/(?P<id>[0-9]+)/$', views.edit, name='edit'),
	url('^delete/(?P<id>[0-9]+)/$', views.delete, name='delete'),
	url('^comment/', views.note_comment, name='note_comment'),
]