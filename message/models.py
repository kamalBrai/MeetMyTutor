from django.db import models
from accounts.models import CustomUser
from profileapp.models import Profile_Student, Profile_Tutor
from requestapp.models import Requesting_tutor



class Message(models.Model):
    """Individual messages in a chat."""
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages",null=True,blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    reciever = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reciever_msg",null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100,default="no_name")

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"From {self.sender.username} at {self.timestamp}"

