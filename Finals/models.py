from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_photos/')

    def __str__(self):
        return f"{self.user.username}'s Image"

class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admission_number = models.CharField(max_length=8,unique=True)
    phone_number = models.CharField(max_length=13,unique=True)
    school_id = models.ImageField(upload_to='user_id/')

    def __str__(self):
        return f"{self.user.username} details"