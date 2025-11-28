from django.urls import path
from profileapp import views

urlpatterns = [
    path('tutor_profile/',views.tutor_profile_view.as_view(),name="tutor_profile"),       
    path('edit_tutor_profile/',views.edit_tutor_profile,name="edit_tutor_profile"),   
    path('student_profile/',views.student_profile_view,name="student_profile"),   
    path('edit_student_profile/',views.edit_student_profile,name="edit_student_profile"),           
]
