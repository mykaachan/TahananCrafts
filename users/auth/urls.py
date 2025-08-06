# users/auth/urls.py

from django.urls import path
from .views import TestAuthConnection
from .views import RegisterView  # Removed TestAuthConnection
from .views import SendEmailOTP, VerifyEmailOTP



urlpatterns = [
    path('test/', TestAuthConnection.as_view(), name='auth-test'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('send-email-otp/', SendEmailOTP.as_view()),
    path('verify-email-otp/', VerifyEmailOTP.as_view()),

    
]
