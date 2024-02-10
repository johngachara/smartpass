from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class Signup(UserCreationForm):
    custom_password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    custom_password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['custom_password1','custom password2']