# users/auth/urls.py

from django.urls import path
from .views import TestAuthConnection
from .views import RegisterView  # Removed TestAuthConnection



urlpatterns = [
    path('test/', TestAuthConnection.as_view(), name='auth-test'),
    path('register/', RegisterView.as_view(), name='auth-register'),

    
]
