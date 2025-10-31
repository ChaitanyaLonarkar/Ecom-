

from django.urls import path

from .auth_views import *

urlpatterns = [
    path('auth/register', RegisterUserView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/profile', UserProfileView.as_view(), name='profile'),
    path('auth/create-admin', CreateAdminView.as_view(), name='create-admin'),


   
]
