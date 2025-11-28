from django.contrib import admin
from accounts.models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class user(admin.ModelAdmin):
    list_display = ['id' ,'first_name', 'last_name', 'username']