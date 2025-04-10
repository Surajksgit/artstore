# artapp/admin.py
from django.contrib import admin

# Register your models here.

from .models import UserProfile, UserDashboard

admin.site.register(UserProfile)
admin.site.register(UserDashboard)
