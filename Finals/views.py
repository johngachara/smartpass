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
        form = Signup(request.POST, request.FILES)
        if form.is_valid():
            user_data = form.cleaned_data
            new_user = form.save(commit=False)  # Get the unsaved user instance

            # Check if the email address ends with the allowed domain
            allowed_domain = '@students.kcau.ac.ke'
            if not user_data['email'].endswith(allowed_domain):
                adm = user_data['adm_no']
                form.add_error('email', f'Please use the school email address {adm}{allowed_domain}.')
                return render(request, 'signup.html', {"Form": form})

            # Check if the adm_no is part of the email address
            if user_data['adm_no'] not in user_data['email']:
                form.add_error('email', 'Please use your individual school email address.')
                return render(request, 'signup.html', {"Form": form})

            # Activate the user and save
            new_user.is_active = True
            new_user.save()

            # Optionally, you can proceed with email verification here

            return redirect('home')

    else:
        form = Signup()

    return render(request, 'signup.html', {"Form": form})


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