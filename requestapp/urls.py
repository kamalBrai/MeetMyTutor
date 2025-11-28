from django.urls import path
from requestapp import views

urlpatterns = [
    path('tutor_session/<int:id>',views.tutor_session_request,name="tutor_session_request"),       
    path('student_request/',views.student_request,name="request_list"),       
    path('tutor_request/',views.tutor_request,name="request_list_tutor"),              
    path('counter_offer/<int:id>',views.counter_offer,name="counter_offer"),       
    path('accept_request/<int:id>',views.accept_request,name="accept_request"),       
    path('edit_request/<int:id>',views.edit_request,name="edit_request"),   
    path('edit_accept_request/<int:id>',views.edit_accept_request,name="edit_accept_request"),    
    path('counteroffer_view/<int:id>',views.counter_offer_view,name="counter_offer_view"),    
]
