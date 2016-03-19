from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

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
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Duty, DutyAdmin)
admin.site.register(BonusPoints, BonusPointsAdmin)