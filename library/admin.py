from django.contrib import admin
from library.models import *
# Register your models here.
admin.site.register(LibraryTagCategory, LibraryTagCategoryAdmin)
admin.site.register(LibraryTag, LibraryTagAdmin)
admin.site.register(LibraryFile, LibraryFileAdmin)