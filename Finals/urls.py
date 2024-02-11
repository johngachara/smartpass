from django.conf.urls.static import static
from django.urls import path

from Finals import views
from djangoProject20 import settings

urlpatterns = [
    path('',views.signup,name="signup"),
    path('photo',views.take_photo,name='photo'),
    path('photo_prev',views.photo_preview,name='photo_prev'),
    path('complete',views.photo_redirect,name='complete'),
    path('home',views.home,name='home'),
    path('verif/<int:user_id>',views.email_verification,name='verif')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)