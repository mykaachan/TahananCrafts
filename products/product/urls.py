from django.urls import path, include
from .views import ProductTestView, AddProductView, DeleteProductView, UpdateProductView, ReadProductView

urlpatterns = [
   path('product-test/',ProductTestView.as_view(), name='product-test'),  # For product-related URLs
   path('add_product/', AddProductView.as_view(), name='add-product'),  # For adding a product
   path('delete_product/', DeleteProductView.as_view(), name='delete-product'),  # For deleting a product
   path('update_product/', UpdateProductView.as_view(), name='update-product'),  # For updating a product
   path('read_product/', ReadProductView.as_view(), name='read-product'),  # For reading a product
]


