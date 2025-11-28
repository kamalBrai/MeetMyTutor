from django.urls import path
from findtutor import views

urlpatterns = [
    path('all-tutor/',views.all_tutor_view,name="all_tutor"),       
    path('nearest-tutors-list/', views.nearest_tutors_list_view, name="nearest_tutors_list"),
    path('detect-location/', views.detect_location_view, name="detect_location"),     
    path('view_profile/<int:id>',views.view_tutor_profile_view,name="view_tutor_profile"),       
    path('view_profile2/<int:id>',views.view_tutor_profile_view2,name="view_tutor_profile2"),       
    path('view_student_profile/<int:id>',views.view_student_profile,name="view_student_profile"),       
]
