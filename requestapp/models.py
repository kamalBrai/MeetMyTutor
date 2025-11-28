from django.db import models
from profileapp.models import Profile_Student, Profile_Tutor

class Requesting_tutor(models.Model):
    MODE_CHOICES = (
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    )
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='Online')
    student_user = models.ForeignKey(Profile_Student, on_delete=models.CASCADE, related_name="sent_requests")
    tutor_user = models.ForeignKey(Profile_Tutor, on_delete=models.CASCADE, related_name="recieve_requests")

    # Store multiple subjects as JSON
    subjects = models.JSONField(default=list, blank=True)

    proposed_rate = models.IntegerField()
    session_start_date = models.DateField()
    session_end_date = models.DateField()
    session_time_from = models.TimeField()
    session_time_to = models.TimeField()
    status = models.CharField(max_length=20, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    # Counter offer fields
    counter_time_from = models.CharField(max_length=100, null=True, blank=True)
    counter_time_to = models.CharField(max_length=100, null=True, blank=True)
    counter_start_date = models.DateField(null=True, blank=True)
    counter_end_date = models.DateField(null=True, blank=True)
    counter_proposed_rate = models.IntegerField(null=True, blank=True)
    is_edit = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    desc = models.TextField(default='no desc', null=True, blank=True)

    def __str__(self):
        return f"{self.student_user.user.username} → {self.tutor_user.user.username}"


# from django.db import models
# from profileapp.models import Profile_Student,Profile_Tutor
# from categories.models import subjects_list

# # Create your models here.
# class Requesting_tutor(models.Model):
#     MODE_CHOICES = (
#         ('Online', 'Online'),
#         ('Offline', 'Offline'),
#     )
#     mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='Online')
#     student_user = models.ForeignKey(Profile_Student,on_delete=models.CASCADE,related_name="sent_requests")
#     tutor_user = models.ForeignKey(Profile_Tutor,on_delete=models.CASCADE,related_name="recieve_requests")
#     subject = models.ManyToManyField(subjects_list)
#     proposed_rate = models.IntegerField()
#     session_start_date = models.DateField()
#     session_end_date = models.DateField()
#     session_time_from = models.TimeField()
#     session_time_to = models.TimeField()
#     status = models.CharField(max_length=20, default='pending') 
#     timestamp = models.DateTimeField(auto_now_add=True)
    
#     # Fields for counter offer
#     counter_time_from = models.CharField(max_length=100, null=True, blank=True)
#     counter_time_to = models.CharField(max_length=100, null=True, blank=True)
#     counter_start_date = models.DateField(null=True, blank=True)
#     counter_end_date = models.DateField(null=True, blank=True)
#     counter_proposed_rate = models.IntegerField(null=True,blank=True)
#     is_edit = models.BooleanField(default=False)
#     is_complete = models.BooleanField(default=False)
#     desc = models.TextField(default='no desc',null=True,blank=True)
#     def __str__(self):
#         return f"{self.student_user.user.username} → {self.tutor_user.user.username}"    