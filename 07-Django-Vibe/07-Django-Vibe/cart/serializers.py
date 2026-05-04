# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
# from catalog.models import ProductVariant

class CartItemSerializer(serializers.ModelSerializer):
    product_variant_sku = serializers.CharField(source='product_variant.sku', read_only=True)
    product_variant_name = serializers.CharField(source='product_variant.name', read_only=True)
    product_name = serializers.CharField(source='product_variant.product.name', read_only=True)
    price = serializers.DecimalField(source='product_variant.price', max_digits=10, decimal_places=2, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product_variant', 'product_variant_sku', 'product_variant_name', 'product_name', 'price', 'quantity', 'total']
        read_only_fields = ['cart', 'added_at']

    def get_total(self, obj):
        return obj.quantity * obj.product_variant.price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'user', 'session_key']

    def get_total_price(self, obj):
        return obj.get_total_price()
