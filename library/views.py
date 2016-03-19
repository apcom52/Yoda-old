from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):
	files = []
	files_list = LibraryFile.objects.all().order_by('-id')

	for file in files_list:
		files.append({
			'id': file.id,
			'title': file.title,
			'icon': get_file_ext_image(file.file.name)
			})

	context = {
		'title':'Библиотека',
		'files': files,
	}
	return render(request, 'library_index.html', context)




def get_file_ext_image(file):
	icon_url = '/media/img/fileformat/etc.png'
	extensions = (
		'7z',		'apk',		'avi',		'bmp',
		'css',		'dll',		'doc',		'docx',
		'exe',		'flv',		'gif',		'gz',
		'html',		'iso',		'jar',		'jpg',
		'js',		'mov',		'mp3',		'mp4',
		'mpeg',		'pdf',		'php',		'png',
		'ppt',		'ps',		'psd',		'rar',		'svg',
		'swf',		'tar',		'txt',		'wav',		'zip'
	)

	for ext in extensions:
		if file.endswith('.' + ext):
			return '/media/img/fileformat/' + ext + '.png'
	return icon_url