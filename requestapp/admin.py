from django.contrib import admin
from requestapp.models import Requesting_tutor
# Register your models here.

@admin.register(Requesting_tutor)
class request_tutor(admin.ModelAdmin):
    list_display = ['id', 'get_student_name', 'get_tutor_name', 'mode' , 'status', 'is_edit']

    def get_student_name(self, obj):
        return f"{obj.student_user.user.first_name} {obj.student_user.user.last_name}"
    get_student_name.short_description = "Student Name"

    def get_tutor_name(self, obj):
        return f"{obj.tutor_user.user.first_name} {obj.tutor_user.user.last_name}"
    get_tutor_name.short_description = "Tutor Name"
