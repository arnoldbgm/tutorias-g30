# orders/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart, CartItem
from catalog.models import ProductVariant
from users.models import User # Needed for user FK
from addresses.models import Address # Might be needed if Address model is used directly
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal

class OrderItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing order items.
    Typically accessed through the OrderViewSet.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAdminUser] # Usually managed via Order creation

    def get_queryset(self):
        """
        Filter order items by order if an order ID is provided in the URL.
        """
        queryset = OrderItem.objects.all()
        order_pk = self.kwargs.get('order_pk') # Assuming URL pattern includes order_pk
        if order_pk:
            queryset = queryset.filter(order_id=order_pk)
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing orders.
    Users can view their own orders, admins can view all.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Create an order from the user's current cart.
        This involves a transaction to ensure atomicity.
        """
        user = self.request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'detail': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        if not cart.items.exists():
            return Response({'detail': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch shipping and billing addresses (as JSON snapshots)
        # The prompt suggests JSON snapshot, so we won't directly link to Address model here,
        # but would typically fetch the selected address and serialize it.
        # For now, we'll leave them as null, to be populated by frontend or assumed.
        # In a real app, you'd select an address and pass its data.
        shipping_address_data = None
        billing_address_data = None
        
        # Attempt to get default address for snapshot if available, otherwise use null
        default_address = Address.objects.filter(user=user, is_default=True).first()
        if default_address:
            # Basic snapshot, could be more detailed
            shipping_address_data = {
                'full_name': default_address.full_name,
                'address_line_1': default_address.address_line_1,
                'address_line_2': default_address.address_line_2,
                'city': default_address.city,
                'state': default_address.state,
                'country': default_address.country,
                'postal_code': default_address.postal_code,
            }
            billing_address_data = shipping_address_data # Usually same as shipping for e-commerce

        total_amount = Decimal('0.00')
        order_items_data = []

        with transaction.atomic():
            # Create the Order instance first
            order = serializer.save(
                user=user,
                shipping_address=shipping_address_data,
                billing_address=billing_address_data,
                # status will be set to 'pending' by default
            )

            # Create OrderItems from CartItems
            for item in cart.items.all():
                # Ensure product_variant still exists and is active
                try:
                    product_variant = ProductVariant.objects.get(pk=item.product_variant_id, is_active=True)
                except ProductVariant.DoesNotExist:
                    # Handle case where product variant is no longer available
                    # Rollback transaction and return error
                    transaction.set_rollback(True)
                    return Response({'detail': f'Product variant {item.product_variant.sku} is no longer available.'}, status=status.HTTP_400_BAD_REQUEST)

                item_price = product_variant.price
                item_total = item.quantity * item_price
                total_amount += item_total

                OrderItem.objects.create(
                    order=order,
                    product_variant=product_variant,
                    product_name=item.product_variant.product.name, # Snapshot
                    sku=product_variant.sku,                       # Snapshot
                    price=item_price,
                    quantity=item.quantity,
                    total=item_total
                )

            # Update the order's total amount
            order.total_amount = total_amount
            order.save()

            # Clear the cart after order creation
            cart.items.all().delete()
            cart.updated_at = timezone.now()
            cart.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        """
        Admin action to update the status of an order.
        """
        order = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response({'detail': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add validation for allowed status transitions if necessary
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)

    # Add other actions like view_order_items, etc. if needed
