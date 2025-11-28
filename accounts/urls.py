from django.urls import path
from accounts import views

urlpatterns = [
    path('register/',views.Register.as_view(),name="register"),    
    path('login/',views.Log_in.as_view(),name="log_in"),    
    path('logout/',views.log_out,name="log_out"),    
]
