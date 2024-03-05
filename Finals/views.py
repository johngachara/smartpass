import base64
import random
from io import BytesIO

import qrcode
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserPhoto
from .serializers import UserPhotoSerializer, UserSerializer

from Finals.forms import Signup, signin_form, UserImageForm
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
                form.add_error('email', f'Please use the school email address {adm}{allowed_domain}')
                return render(request, 'signup.html', {"Form": form})

            # Check if the adm_no is part of the email address
            if user_data['adm_no'] not in user_data['email']:
                form.add_error('email', 'Please use your individual school email address.')
                return render(request, 'signup.html', {"Form": form})

            if User.objects.filter(email=user_data['email']).exists():
                form.add_error('email', 'This email is already in use')
                return render(request, 'signup.html', {"Form": form})
            new_user.is_active = False
            new_user.save()

            # Optionally, you can proceed with email verification here
            return redirect('verif', new_user.id)

    else:
        form = Signup()

    return render(request, 'signup.html', {"Form": form})


def email_verification(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'email.html', {"User": user})


def verify_email(request, user_id):
    user = User.objects.get(pk=user_id)
    sender_email = settings.EMAIL_HOST_USER
    heading = "Your verification code"
    recipient_email = user.email
    verification_code = str(random.randint(100000, 999999))
    request.session['verification_code'] = verification_code
    email_content = f"Your Verification code is {verification_code}"
    mail = send_mail(heading, email_content, sender_email, [recipient_email])
    return redirect('code', user.id)


def verify_code(request, user_id):
    user = User.objects.get(pk=user_id)
    stored_verification_code = request.session.get('verification_code')
    if request.method == 'POST':
        submitted_code = request.POST.get('verification_code')
        if submitted_code == stored_verification_code:
            del request.session['verification_code']
            return redirect('bind', user.id)
        else:

            return render(request, 'verify.html', {"User_id": user.id})

    return render(request, 'verify.html', {"User_id": user.id})


def await_verification(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.is_active == False:
        return HttpResponse('Awaiting verification')
    else:
        return redirect('convert_to_qr', user.id)


def bind_device(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'bind.html', {"User": user})


def take_photo(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'photo.html', {"User": user})


def photo_preview(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'photo_prev.html', {"User": user})


def photo_redirect(request, user_id):
    user = User.objects.get(pk=user_id)
    return redirect('await', user.id)


@api_view(['POST'])
def upload_photo(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    photo_data = request.data.get('photo')
    serializer = UserPhotoSerializer(data={'user': user.id, 'photo': photo_data})

    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        new_photo = UserPhoto(user=user, photo=data['photo'])
        new_photo.save()

        return Response({'message': 'Photo uploaded successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def signin(request):
    form = signin_form()
    if request.method == 'POST':
        form = signin_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Use authenticate to check if the provided credentials are valid
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active == False:
                    return render(request, 'await.html')
                else:
                    login(request, user)
                    return redirect('convert_to_qr', user.id)
            else:
                # Invalid credentials, show an error message
                form = signin_form()
                messages.error(request, 'Incorrect username or password')
    return render(request, 'signin.html', {"form": form})


def convert_to_qr(request, user_id):
    instance = get_object_or_404(User, pk=user_id)
    if instance.is_active == False:
        return render(request, 'await.html')
    instance_photo = UserPhoto.objects.filter(user=instance).first()
    data_to_encode = f"{instance.username} {instance.first_name} {instance.last_name} {instance_photo} "  # Customize based on your model fields
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a BytesIO object
    img_bytesio = BytesIO()
    img.save(img_bytesio)
    img_bytesio.seek(0)
    img_base64 = base64.b64encode(img_bytesio.read()).decode('utf-8')

    # Pass the base64-encoded image data to the template
    context = {'qr_code': img_base64, 'user': instance}
    return render(request, 'home.html', context)


def qr(request):
    return render(request, 'qr.html')


def await_verification(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.is_active == False:
        return render(request, 'await.html')
    else:
        return redirect('convert_to_qr', user.id)

#For Serverside
def activate_user_page(request):
    users = User.objects.filter(is_active=False)
    return render(request, 'activate_user_page.html', {'users': users})

#For serverSide
def view_inactive_user(request, user_id):
    user = User.objects.get(pk=user_id)
    picture = UserPhoto.objects.filter(user=user).first()

    return render(request, 'view_user.html', {"user": user, "picture": picture})
#For Serverside
def decline_inactive_user(request, user_id):
    user = User.objects.get(pk=user_id)
    sender_email = settings.EMAIL_HOST_USER
    heading = "Account Declined"
    recipient_email = user.email
    email_content = "Your account has been declined as your provided details do not match.Try signing up again with the correct details."
    mail = send_mail(heading, email_content, sender_email, [recipient_email])
    user.delete()
    return redirect('activate')

#For Serverside
def activate_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect('activate')
def wrong_device(request):
    return render(request, 'error.html')


def show_photos(request):
    photos = UserPhoto.objects.all()
    return render(request,'show_photo.html', {"photos": photos})


#For serverless
@api_view(['GET'])
def get_inactive_users(request):
    if request.method == 'GET':
        users = User.objects.filter(is_active=False)
        serializer = UserSerializer(instance=users, many=True)
        return Response({"data":serializer.data})


#For Serverless
@api_view(['GET'])
def get_inactive_user(request, id):
    try:
        user = User.objects.get(pk=id)
        serializer = UserSerializer(instance=user)
        user_photo = UserPhoto.objects.filter(user=user).first()
        serializer2 = UserPhotoSerializer(instance=user_photo)
        return Response({"user_data": serializer.data, "user_photo_data": serializer2.data})
    except User.DoesNotExist:
        return Response({"Error": "User with the given id not found"})


#For Serverless
@api_view(['PUT'])
def activate_users(request, id):
    if request.method == 'PUT':
        user = User.objects.get(pk=id)
        user.is_active = True
        user.save()
        return Response({"message": "User activated"})

#for serverside
@api_view(['DELETE'])
def deactivate_users(request, id):
    if request.method == 'DELETE':
        user = User.objects.get(pk=id)
        user.delete()
        return Response({"message": "User deleted"})

@api_view(['GET'])
def get_active_users(request):
    if request.method == 'GET':
        users = User.objects.filter(is_active=True)
        serializer = UserSerializer(instance=users, many=True)
        return Response({"users": serializer.data})

@api_view(['PUT'])
def deactivate(request, id):
    if request.method == 'PUT':
        user = User.objects.get(pk=id)
        user.is_active = False
        user.save()
        return Response({'Message': 'User deactivated'})