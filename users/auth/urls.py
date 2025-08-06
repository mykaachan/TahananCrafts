# users/auth/urls.py

from django.urls import path, include
from .views import TestAuthConnection
from .views import UserRegistrationView # Removed TestAuthConnection
from .views import VerifyRegisterOTPView
from .views import LoginRequestOTPView, LoginVerifyOTPView



urlpatterns = [
    path('test/', TestAuthConnection.as_view(), name='auth-test'),
    path('register/', UserRegistrationView.as_view(), name='auth-register'),
    path('verify-email-otp/', VerifyRegisterOTPView.as_view()),
    path('login/',LoginRequestOTPView.as_view(), name='auth-login'),
    path('login-verify-otp/', LoginVerifyOTPView.as_view(), name='auth-login-verify-otp'),
]


