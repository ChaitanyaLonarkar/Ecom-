

from django.urls import path

from .auth_views import *

urlpatterns = [
    path('auth/register', RegisterUserView.as_view(), name='register'),
   
]
