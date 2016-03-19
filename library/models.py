from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class LibraryTagCategory(models.Model):
	title = models.CharField('Название категории тега', max_length = 128)
	color = models.CharField('Цвет категории', max_length = 16)
	class Meta():
		verbose_name = 'Категория тегов'
		verbose_name_plural = 'Категории тегов'

	def __str__(self):
		return self.title

class LibraryTagCategoryAdmin(admin.ModelAdmin):
	list_display = ('title',)


class LibraryTag(models.Model):
	title = models.CharField('Название тега', max_length = 64)
	tag_category = models.ForeignKey(LibraryTagCategory)
	views = models.IntegerField('Количество просмотров', default = 0)

	def __str__(self):
		return self.title

	class Meta():
		verbose_name = 'Тег библиотеки'
		verbose_name_plural = 'Теги библиотеки'


class LibraryTagAdmin(admin.ModelAdmin):
	list_display = ('title', 'tag_category')


class LibraryFile(models.Model):
	login = models.ForeignKey(User)
	title = models.CharField('Название файла', max_length = 128)
	description = models.TextField('Описание файла', null = True, blank = True)
	file = models.FileField(upload_to = 'uploads/%Y/%m/%d')
	tags = models.ManyToManyField(LibraryTag, blank = True)
	pub_date = models.DateTimeField('Дата публикации', editable = False, null = True, blank = True)
	views = models.IntegerField('Количество просмотров', default = 0)
	downloads = models.IntegerField('Количество загрузок', default = 0)
	is_available = models.BooleanField('Файл доступен для загрузки', default = True)

	def __str__(self):
		return self.title

	class Meta():
		verbose_name = 'Файл библиотеки'
		verbose_name_plural = 'Файлы библиотеки'

class LibraryFileAdmin(admin.ModelAdmin):
	fields = ('title', 'description', 'login', 'file', 'tags', 'is_available')
	list__display = ('title', 'login', 'file', 'pub_date')