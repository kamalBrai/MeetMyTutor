from django.urls import path
from mystudentsapp import views

urlpatterns = [
    path('incomplete/',views.mystudents,name="mystudents"),       
    path('is_complete/<int:id>',views.is_complete_view,name="complete"),       
    path('completed/',views.completed_view,name="completed"),       
    path('all_students/',views.all_students,name="all_students"),       
]
