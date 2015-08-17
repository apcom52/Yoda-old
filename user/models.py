from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	avatar = models.ImageField(upload_to='img/%Y/%m/%d/', verbose_name='Фотография пользователя', default='img/2015/08/04/ufo.jpg')
	facebook = models.CharField('Facebook', max_length = 256, blank = True, null = True)
	twitter = models.CharField('Twitter', max_length = 256, blank = True, null = True)
	vk = models.CharField('ВКонтакте', max_length = 256, blank = True, null = True)
	phone = models.CharField('Номер телефона', max_length = 16, blank = True, null = True)
	#def __str__(self):
	#	return self.user

	class Meta:
		verbose_name = 'Профиль'
		verbose_name_plural = 'Профили'