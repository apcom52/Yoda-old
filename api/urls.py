from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from . import views

'''router = DefaultRouter()
router.register(r'library/file', views.LibraryFilesAPI)
router.register(r'library/tag', views.LibraryTagAPI)
router.register(r'user', views.UserAPI)'''

urlpatterns = [
	#url(r'^library-file/$', LibraryFileList.as_view(), name='library-file-list'),	
	#url('^library/file', views.library_files, name='library_files'),
	url('^library/file', views.LibraryFilesAPI.as_view()),
	url('^library/tags', views.LibraryTagAPI.as_view()),
	url('^library/tag-category', views.library_tag_category, name='library_tag_category'),

	url('^users/$', views.UserAPI.as_view()),
	url('^users/attendances', views.AttendanceAPI.as_view()),

	url('^notes/', views.NoteAPI.as_view()),

	url('^favorite/$', views.FavoriteAPI.as_view()),

	url('^settings/$', views.SettingsAPI.as_view()),
	
	url('^timetable/$', views.TimetableAPI.as_view()),

	url('^blog/$', views.BlogPostAPI.as_view()),
	#url('^', include(router.urls)),
]