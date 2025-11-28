# in signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # or your custom user model
from profileapp.models import Profile_Student

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        Profile_Student.objects.create(user=instance)
