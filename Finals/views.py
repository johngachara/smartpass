from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('photo_prev')
    else:
        form = UserCreationForm()
    return render(request,'signup.html',{"Form":form})
def take_photo(request):
    return render(request,'photo.html')

def photo_preview(request):
    return render(request,'photo_prev.html')

def photo_redirect(request):
    return redirect('home')
def home(request):
    return render(request,'home.html')