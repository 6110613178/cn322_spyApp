from django.contrib import admin
from .models import UserProfile , Mission , RSAKey , MissionAdmin

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Mission)
admin.site.register(RSAKey)
admin.site.register(MissionAdmin)