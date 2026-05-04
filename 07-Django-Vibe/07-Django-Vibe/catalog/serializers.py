# catalog/serializers.py
from rest_framework import serializers
from .models import Category, Product, ProductVariant, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'alt_text', 'is_main', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'sku', 'name', 'price', 'compare_price', 'stock', 'weight', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    stock_count = serializers.IntegerField(source='get_stock_count', read_only=True) # Custom field for stock count

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'category', 'brand', 'is_active', 'variants', 'images', 'stock_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
