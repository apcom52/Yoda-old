from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserInline(admin.StackedInline):
	model = UserProfile
	can_delete = True
	verbose_name_plural = 'Дополнительно'

#Новый класс настроек для User
class UserAdmin(UserAdmin):
	inlines = (UserInline, )

#Перерегистрация модели User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)