from django.urls import path,include
from .views import UserRegistration
from django.views.generic import TemplateView


urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('register/',UserRegistration.as_view(), name='user-register'),
    path('my-account/',TemplateView.as_view(template_name='registration/user_detail.html'),name='my-account'),
    path('register/success',TemplateView.as_view(template_name='registration/user_registration_success.html'),name='registration-success')
]
