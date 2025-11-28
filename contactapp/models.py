from django.db import models


# Create your models here.
class Contactmodel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()