# shipments/serializers.py
from rest_framework import serializers
from .models import Shipment
# from orders.models import Order

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
