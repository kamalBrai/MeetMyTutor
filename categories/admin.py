from django.contrib import admin
from .models import districts,subjects_list
# Register your models here.

@admin.register(districts)
class District(admin.ModelAdmin):
    list_display = ['id','name']
    
@admin.register(subjects_list)
class Subjects(admin.ModelAdmin):
    list_display = ['id','subject_name']
    