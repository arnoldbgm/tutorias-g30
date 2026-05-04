# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
# from users.models import User
# from addresses.models import Address
# from catalog.models import ProductVariant

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(read_only=True)
    sku = serializers.CharField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product_variant', 'product_name', 'sku', 'price', 'quantity', 'total']
        read_only_fields = ['order', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    # user = serializers.PrimaryKeyRelatedField(read_only=True) # For now, user is set by view
    # shipping_address = serializers.JSONField(read_only=True) # Can be updated if needed
    # billing_address = serializers.JSONField(read_only=True) # Can be updated if needed

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_amount', 'shipping_address', 'billing_address', 'items', 'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'total_amount', 'created_at', 'updated_at', 'items']

    # We will add logic to create OrderItems from cart in the view/service layer
