from rest_framework import serializers
from .models import UserPhoto

class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = ['user', 'photo']