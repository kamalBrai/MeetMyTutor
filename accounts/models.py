from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_type = (
        ('student', 'student'),
        ('tutor', 'tutor'),
    )
    email = models.EmailField(unique=True)
    usertype = models.CharField(max_length=100,choices=user_type,null=False,blank=False,default='student')


