from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_photos/')