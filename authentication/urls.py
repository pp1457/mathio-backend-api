from django.urls import path, include
from . import views 
from rest_framework import routers

urlpatterns = [
    path('users/', views.UserListView.as_view()),
    path('users/<int:pk>/', views.UserDetailView.as_view()),
    path('register/', views.UserRegisterView.as_view()),
    path('', include('rest_framework.urls')),
]
