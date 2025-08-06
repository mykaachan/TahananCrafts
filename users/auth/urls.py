# users/auth/urls.py

from django.urls import path
from .views import TestAuthConnection
from .views import UserRegistrationView # Removed TestAuthConnection
from .views import VerifyOTPView



urlpatterns = [
    path('test/', TestAuthConnection.as_view(), name='auth-test'),
    path('register/', UserRegistrationView.as_view(), name='auth-register'),
    path('verify-email-otp/', VerifyOTPView.as_view()),

    
]
