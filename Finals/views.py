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

            if User.objects.filter(email=user_data['email']).exists():
                form.add_error('email', 'This email is already in use')
                return render(request, 'signup.html', {"Form": form})

            new_user.save()
            # Optionally, you can proceed with email verification here
            return redirect('verif',new_user.id)

    else:
        form = Signup()

    return render(request, 'signup.html', {"Form": form})


def email_verification(request,user_id):
    user = User.objects.get(pk=user_id)
    return render(request,'email.html',{"User":user})


def verify_email(request,user_id):
    user = User.objects.get(pk=user_id)
    sender_email = settings.EMAIL_HOST_USER
    heading = "Your verification code"
    recipient_email = user.email
    verification_code = str(random.randint(100000, 999999))
    request.session['verification_code'] = verification_code
    email_content = f"Your Verification code is {verification_code}"
    mail = send_mail(heading,email_content, sender_email, [recipient_email])
    return redirect('code',user.id)

def verify_code(request,user_id):
    user = User.objects.get(pk=user_id)
    stored_verification_code = request.session.get('verification_code')
    if request.method == 'POST':
        submitted_code = request.POST.get('verification_code')
        if submitted_code == stored_verification_code:
            # Code is correct, perform necessary actions (e.g., activate the user)
            user.is_active = True
            user.save()


            # Clear the verification code from the session
            del request.session['verification_code']
            return redirect('home')
        else:
            return render(request, 'verify.html', {"User_id": user.id})

    return render(request,'verify.html',{"User_id":user.id})


def bind_device(request):
    return render(request,'bind.html')
def take_photo(request):
    return render(request,'photo.html')

def photo_preview(request):
    return render(request,'photo_prev.html')

def photo_redirect(request):
    return redirect('home')
def home(request):
    return render(request,'home.html')