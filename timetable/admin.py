from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Control, ControlAdmin)
admin.site.register(NewPlace, NewPlaceAdmin)
admin.site.register(TeacherTimetable, TeacherTimetableAdmin)
admin.site.register(NotStudyTime, NotStudyTimeAdmin)
admin.site.register(TransferredLesson, TransferredLessonAdmin)
admin.site.register(CanceledLesson, CanceledLessonAdmin)
admin.site.register(Lesson_Item, Lesson_ItemAdmin)