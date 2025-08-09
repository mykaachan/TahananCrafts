from django.urls import path, include
from .views import ProductTestView, AddProductView

urlpatterns = [
   path('product-test/',ProductTestView.as_view(), name='product-test'),  # For product-related URLs
   path('add_product/', AddProductView.as_view(), name='add-product'),  # For adding a product
]


