from django.db import models
from accounts.models import CustomUser
from profileapp.models import *
from requestapp.models import Requesting_tutor
# Create your models here.
class Feedback(models.Model):
    tutor_user = models.ForeignKey(Profile_Tutor,on_delete=models.CASCADE)
    student_user = models.ForeignKey(Profile_Student,on_delete=models.CASCADE)
    req_tutor = models.ForeignKey(Requesting_tutor,on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_feedback = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_user.user.username} rated {self.tutor_user.user.username} - {self.rating} Stars"