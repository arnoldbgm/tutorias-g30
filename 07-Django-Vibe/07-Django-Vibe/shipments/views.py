# shipments/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Shipment
from .serializers import ShipmentSerializer
from orders.models import Order # Need to link shipment to order

class ShipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing shipments.
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated] # Requires authentication

    def get_queryset(self):
        """
        Filter shipments to show only those related to the user's orders, or all for admins.
        """
        user = self.request.user
        if user.is_staff:
            return Shipment.objects.all()
        return Shipment.objects.filter(order__user=user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Action to update shipment status.
        """
        shipment = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response({'detail': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update status and timestamps
        shipment.status = new_status
        if new_status.lower() == 'shipped' and not shipment.shipped_at:
            shipment.shipped_at = timezone.now()
        elif new_status.lower() == 'delivered' and not shipment.delivered_at:
            shipment.delivered_at = timezone.now()
        
        shipment.updated_at = timezone.now()
        shipment.save()

        # Optionally update the associated order status as well
        order = shipment.order
        if order.status != 'shipped' and new_status.lower() == 'shipped':
            order.status = 'shipped'
            order.save()
        elif order.status != 'delivered' and new_status.lower() == 'delivered':
            order.status = 'delivered'
            order.save()

        return Response(ShipmentSerializer(shipment).data)

    # Action to create shipment might be called after payment is confirmed
    # or manually by an admin.
