from django.urls import path, include
from .views import UserList, UserDetail, UserRegisterView
from rest_framework import routers

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('', include('rest_framework.urls')),
]
