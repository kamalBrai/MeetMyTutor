from django.urls import path
from contactapp import views

urlpatterns = [
    path('contactus/',views.Contact_Page.as_view(),name="contact"),       
]
