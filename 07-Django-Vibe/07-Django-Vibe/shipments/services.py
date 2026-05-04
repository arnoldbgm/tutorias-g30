# shipments/services.py
from .models import Shipment
from .serializers import ShipmentSerializer
from orders.models import Order
from django.utils import timezone
from django.db import transaction

class ShipmentService:
    def __init__(self):
        self.shipment_model = Shipment
        self.order_model = Order
        self.shipment_serializer = ShipmentSerializer

    def get_user_shipments(self, user):
        # Returns shipments related to the user's orders
        shipments = self.shipment_model.objects.filter(order__user=user)
        serializer = self.shipment_serializer(shipments, many=True)
        return serializer.data

    def get_shipment_detail(self, user, shipment_id):
        try:
            shipment = self.shipment_model.objects.get(pk=shipment_id, order__user=user)
            serializer = self.shipment_serializer(shipment)
            return serializer.data
        except self.shipment_model.DoesNotExist:
            raise ValueError("Shipment not found.")

    def create_shipment_for_order(self, order, tracking_number=None, carrier=None):
        """
        Creates a pending shipment record for an order.
        This is typically done after the order is paid.
        """
        if self.shipment_model.objects.filter(order=order).exists():
            raise ValueError("Shipment already exists for this order.")
        
        shipment = self.shipment_model.objects.create(
            order=order,
            tracking_number=tracking_number,
            carrier=carrier,
            status='pending',
        )
        return shipment

    def update_shipment_status(self, shipment, new_status):
        """
        Updates the shipment status and potentially the associated order status.
        """
        shipment.status = new_status
        
        # Update timestamps and potentially order status
        if new_status.lower() == 'shipped' and not shipment.shipped_at:
            shipment.shipped_at = timezone.now()
            if shipment.order.status not in ['shipped', 'delivered', 'cancelled']:
                shipment.order.status = 'shipped'
                shipment.order.save()
        elif new_status.lower() == 'delivered' and not shipment.delivered_at:
            shipment.delivered_at = timezone.now()
            if shipment.order.status not in ['delivered', 'cancelled']:
                shipment.order.status = 'delivered'
                shipment.order.save()
        
        shipment.updated_at = timezone.now()
        shipment.save()

        return self.shipment_serializer(shipment).data

# Example usage:
# from orders.models import Order
# shipment_service = ShipmentService()
# order = Order.objects.get(pk=1, status='paid') # Assume order is paid
# shipment = shipment_service.create_shipment_for_order(order, tracking_number='1Z999AA10123456784', carrier='UPS')
# updated_shipment_data = shipment_service.update_shipment_status(shipment, 'shipped')
