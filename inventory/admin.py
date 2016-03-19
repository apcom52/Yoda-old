from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Smile)
admin.site.register(SmileCollection)
admin.site.register(Background)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemCollection)
admin.site.register(UserInventoryItem, UserInventoryItemAdmin)
admin.site.register(Catapult, CatapultAdmin)