from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Action, ActionAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(AchUnlocked, AchUnlockedAdmin)
admin.site.register(Rank, RankAdmin)