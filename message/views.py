from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  Message
from django.db.models import Q ,Max
from accounts.models import CustomUser
from requestapp.models import * 
from profileapp.models import *

@login_required
def chat_list_view(request):
    user = request.user

    # Get all users who have messages with current user
    messages = Message.objects.filter(Q(sender=user) | Q(reciever=user))

    # Annotate latest message timestamp for each chat
    chat_users = {}
    for msg in messages.order_by('-timestamp'):
        other_user = msg.sender if msg.sender != user else msg.reciever
        # Only keep first (latest) message per user
        if other_user.id not in chat_users:
            chat_users[other_user.id] = {
                'user': other_user,
                'last_message': msg,
            }

    chats = list(chat_users.values())

    return render(request, 'message/chat_list.html', {'chats': chats, 'current_user': user})

@login_required
def chatpage_view(request, other_user_id):
    """
    Renders a chat page between the logged-in user and another CustomUser.
    `other_user_id` is the id of the user you want to chat with.
    """
    current_user = request.user
    other_user = get_object_or_404(CustomUser, id=other_user_id)

    # Prevent users from chatting with themselves
    if current_user.id == other_user.id:
        return render(request, "message/error.html", {"message": "Cannot chat with yourself."})
    
    try:
        if current_user.usertype == "student":
            current_profile = Profile_Student.objects.get(user=current_user)
        else:
            current_profile = Profile_Tutor.objects.get(user=current_user)
    except:
        current_profile = None

    try:
        if other_user.usertype == "student":
            other_profile = Profile_Student.objects.get(user=other_user)
        else:
            other_profile = Profile_Tutor.objects.get(user=other_user)
    except:
        other_profile = None
    
        # Get chat history between current_user and other_user
    messages = Message.objects.filter(
        (Q(sender=current_user) & Q(reciever=other_user)) |
        (Q(sender=other_user) & Q(reciever=current_user))
    ).order_by('timestamp')  # oldest first

    context = {
        "other_user": other_user,
        "messages" : messages,
        "current_user" : current_user,
        "other_profile" : other_profile,        
    }
    return render(request, "message/chatpage.html", context)