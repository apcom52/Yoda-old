"""yoda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url('^admin/', include(admin.site.urls)),
    url('^notes/', include('notes.urls')),
    url('^auth/', include('auth.urls')),
    url('^polls/', include('polls.urls')),
    url('^users/', include('user.urls')),
    url('^events/', include('events.urls')),
    url('^files/', include('library.urls')),
    url('^api/', include('api.urls')),
    url('^', include('timetable.urls')),
]

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)