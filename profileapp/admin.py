from django.contrib import admin
from profileapp.models import *
# Register your models here.

@admin.register(Profile_Tutor)
class tutor(admin.ModelAdmin):
    list_display = ['id', 'get_name' , 'qualification', 'longitude' , 'latitude']
    
    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_name.short_description = "Full Name"
    
@admin.register(Profile_Student)
class student(admin.ModelAdmin):
    list_display = ['id', 'get_name' , 'grade' ]
    
    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_name.short_description = "Full Name"