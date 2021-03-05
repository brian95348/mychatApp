from django.contrib import admin
from django.urls import path,include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProfileList, ChatMessages, ChatMessageDetail, UserSignUp, ProfileCreate, ProfileDetail
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    re_path(r'^chats/$',ProfileList.as_view(),name='api-chats'),
    re_path(r'^chats/(?P<username>[\w-]+)/messages/$',ChatMessages.as_view(),name='api-chat'),
    re_path(r'^chats/(?P<username>[\w-]+)/(?P<pk>\d+)/$',ChatMessageDetail.as_view(),name='api-chat-message'),
    path('user/create-profile/',ProfileCreate.as_view(),name='api-profile-create'),
    re_path(r'^chats/(?P<username>[\w-]+)/$',ProfileDetail.as_view(),name='api-profile-detail'),
    path('user/sign-up/',UserSignUp.as_view(),name='api-user-signup'),
    path('user/get-token/',obtain_auth_token,name='api-get-auth-token'),
    path('auth/',include('rest_framework.urls')),
]
