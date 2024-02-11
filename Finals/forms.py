from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class Signup(UserCreationForm):
    adm_no = forms.CharField(max_length=8)
    email = forms.EmailField(label="Student email",required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    student_id = forms.ImageField(required=True)




    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'adm_no', 'first_name', 'last_name','student_id']