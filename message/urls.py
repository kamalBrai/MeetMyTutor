from django.urls import path
from .views import chat_list_view,chatpage_view


urlpatterns = [
    path('message/', chat_list_view, name='chatlist'),
    path('personalchat/<int:other_user_id>',chatpage_view , name='personal_chat'),
]
