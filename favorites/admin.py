from django.contrib import admin
from .models import Favorite, FavoriteAdmin

# Register your models here.
admin.site.register(Favorite, FavoriteAdmin)