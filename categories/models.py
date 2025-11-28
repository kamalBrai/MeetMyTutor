from django.db import models

# Create your models here.
class districts(models.Model):
    name = models.CharField(max_length=50)

class subjects_list(models.Model):
    subject_name = models.CharField(max_length=100)


