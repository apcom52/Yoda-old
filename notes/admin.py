from django.contrib import admin
from notes.models import *

# Register your models here.
admin.site.register(Note, NoteAdmin)
admin.site.register(NoteComment, NoteCommentAdmin)