from django.urls import path

from Finals import views

urlpatterns = [
    path('',views.signup,name="signup"),
    path('photo',views.take_photo,name='photo'),
    path('photo_prev',views.photo_preview,name='photo_prev'),
    path('complete',views.photo_redirect,name='complete'),
    path('home',views.home,name='home')
]