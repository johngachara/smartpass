import random

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from Finals.forms import  Signup
from djangoProject20 import settings


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = Signup(request.POST , request.FILES)
        if form.is_valid():
            user = form.cleaned_data
            new_user = form.save()
            new_user.is_active = False
            forb = '@students.kcau.ac.ke'
            if not user['email'].endswith(forb):
                adm = user['adm_no']
                form.add_error('email', f'please use the school Email address {adm}{forb}.')
                return render(request, 'signup.html', {"Form": form})
            elif user['adm_no'] not in user['email']:
                form.add_error('email', f'please use your individual school Email address ".')
                return render(request, 'signup.html', {"Form": form})
            else:
                new_user.is_active = True
                return redirect('home')
    else:
        form = Signup()

    return render(request,'signup.html',{"Form":form})


def email_verification(request,user_id):
    user = User.objects.get(pk=user_id)
    return HttpResponse(f"{user} found")


def take_photo(request):
    return render(request,'photo.html')

def photo_preview(request):
    return render(request,'photo_prev.html')

def photo_redirect(request):
    return redirect('home')
def home(request):
    return render(request,'home.html')