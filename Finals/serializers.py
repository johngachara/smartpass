from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserPhoto, UserDetails


class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = ['user', 'photo']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','username']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['user','admission_number','phone_number','school_id']