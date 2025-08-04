# users/auth/urls.py

from django.urls import path
from .views import TestAuthConnection

urlpatterns = [
    path('test/', TestAuthConnection.as_view(), name='auth-test'),
]
