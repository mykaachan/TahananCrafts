from rest_framework import serializers  # For creating API serializers
from products.models import Product, Category, Material, ProductImage

# Serializer for additional product images
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']  # Only include the image field

# Main serializer for Product creation and representation
class ProductSerializer(serializers.ModelSerializer):
    # Allow selecting multiple categories and materials by their IDs
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    materials = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all(), many=True)
    # Accept multiple images for the product (besides the main picture)
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'stock_quantity',
            'regular_price', 'sales_price', 'main_picture', 'categories',
            'materials', 'images'
        ]  # Fields to expose in the API

    # Custom create method to handle many-to-many relationships and nested images
    def create(self, validated_data):
        # Extract categories, materials, and images from the validated data
        categories = validated_data.pop('categories')
        materials = validated_data.pop('materials')
        images_data = validated_data.pop('images', [])
        # Create the product instance with the remaining data
        product = Product.objects.create(**validated_data)
        # Set the many-to-many relationships
        product.categories.set(categories)
        product.materials.set(materials)
        # Create associated ProductImage instances for each image
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product  # Return the created product instance