# users/urls.py

from django.urls import path, include

urlpatterns = [
    path('auth/', include('users.auth.urls')),        # For auth/test/
    path('profile/', include('users.profile.urls')),
    path('admin/', include('users.admin.urls')),
]
