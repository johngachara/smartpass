from django.conf.urls.static import static
from django.urls import path

from Finals import views
from djangoProject20 import settings

urlpatterns = [
    path('',views.signup,name="signup"),
    path('photo/<int:user_id>',views.take_photo,name='photo'),
    path('photo_prev/<int:user_id>',views.photo_preview,name='photo_prev'),
    path('complete/<int:user_id>',views.photo_redirect,name='complete'),
    path('verif/<int:user_id>',views.email_verification,name='verif'),
    path('email/<int:user_id>',views.verify_email,name='email'),
    path('code/<int:user_id>',views.verify_code,name='code'),
    path('bind/<int:user_id>',views.bind_device,name='bind'),
    path('api/photo/<int:user_id>/', views.upload_photo, name='upload_photo'),
    path('signin',views.signin,name='signin'),
    path('convert/<int:user_id>/', views.convert_to_qr, name='convert_to_qr'),
    path('qr',views.qr,name='qr'),
    path('await/<int:user_id>',views.await_verification,name='await')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)