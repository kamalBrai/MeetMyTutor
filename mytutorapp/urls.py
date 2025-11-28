from django.urls import path
from . import views

urlpatterns = [
    # Existing URLs
    path('my-tutors/', views.my_tutors_view, name='my_tutors'),
    path('my-tutors/ongoing/', views.mytutors_ongoing, name='my_tutors_ongoing'),
    path('my-tutors/complete/', views.mytutors_complete, name='my_tutors_complete'),
    path('feedback/<int:id>/', views.feedback_view, name='feedback'),
    path('feedback/thankyou/', views.feedback_thankyou, name='feedback_thankyou'),

    # New URL for nearest tutor map
    path('nearest-tutors-map/', views.nearest_tutors_map, name='nearest_tutors_map'),
]
