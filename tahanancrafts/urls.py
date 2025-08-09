from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  # Combined routes for auth, profile, etc.
    path('api/products/', include('products.urls')),  # Combined routes for products and reviews
]
