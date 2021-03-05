from django.urls import path, re_path
from .views import index, ProfileDetailView, ProfileListView, ProfileDeleteView, ProfileUpdateView


urlpatterns = [
    path('',index,name="index"),
    path('chatlist/',ProfileListView.as_view(),name='profile-list'),
    path('chatlist/<slug:username>/',ProfileDetailView.as_view(),name='profile-detail'),
    path('chatlist/<slug:username>/delete/',ProfileDeleteView.as_view(),name='profile-delete'),
    path('chatlist/<slug:username>/update/',ProfileUpdateView.as_view(),name='profile-update')
]
