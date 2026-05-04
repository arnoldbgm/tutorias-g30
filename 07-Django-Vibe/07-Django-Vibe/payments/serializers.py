# payments/serializers.py
from rest_framework import serializers
from .models import Payment
# from orders.models import Order

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'transaction_id', 'paid_at'] # Transaction ID and paid_at are set by provider/payment process
