# orders/services.py
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart, CartItem
from catalog.models import ProductVariant
from users.models import User
from addresses.models import Address
from payments.models import Payment
from shipments.models import Shipment
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal
from django.utils import timezone

class OrderService:
    def __init__(self):
        self.order_model = Order
        self.order_item_model = OrderItem
        self.order_serializer = OrderSerializer
        self.cart_model = Cart
        self.cart_item_model = CartItem
        self.product_variant_model = ProductVariant
        self.user_model = User
        self.address_model = Address
        self.payment_model = Payment
        self.shipment_model = Shipment

    def create_order_from_cart(self, user, shipping_address_data, billing_address_data):
        """
        Creates an order from the user's current cart.
        This is a complex operation requiring a transaction.
        """
        try:
            cart = self.cart_model.objects.get(user=user)
        except self.cart_model.DoesNotExist:
            raise ValueError("Your cart is empty.")

        if not cart.items.exists():
            raise ValueError("Your cart is empty.")

        total_amount = Decimal('0.00')
        order_items_to_create = []

        # --- Address Snapshotting ---
        # Save addresses as JSON snapshots.
        # We expect either pre-saved Address objects or raw data.
        # For this service, we'll assume raw data is passed and we serialize it.
        # A more robust solution might involve validating against Address model first.
        
        # If raw data is passed, serialize it. If Address objects, convert to dict.
        # For simplicity here, assume the data is dict-like.
        snapshot_shipping_address = shipping_address_data
        snapshot_billing_address = billing_address_data

        with transaction.atomic():
            # Create the Order instance
            order = self.order_model.objects.create(
                user=user,
                shipping_address=snapshot_shipping_address,
                billing_address=snapshot_billing_address,
                status='pending', # Default status
                total_amount=Decimal('0.00') # Will be updated later
            )

            # Process cart items and create OrderItems
            for item in cart.items.all():
                try:
                    # Ensure product variant is still active and get its current price
                    product_variant = self.product_variant_model.objects.get(pk=item.product_variant_id, is_active=True)
                    
                    item_price = product_variant.price
                    item_total = item.quantity * item_price
                    total_amount += item_total

                    order_items_to_create.append(
                        self.order_item_model(
                            order=order,
                            product_variant=product_variant,
                            product_name=item.product_variant.product.name, # Snapshot
                            sku=product_variant.sku,                       # Snapshot
                            price=item_price,
                            quantity=item.quantity,
                            total=item_total
                        )
                    )
                except self.product_variant_model.DoesNotExist:
                    # If a variant is no longer available, roll back and raise error
                    transaction.set_rollback(True)
                    raise ValueError(f"Product variant {item.product_variant.sku} is no longer available.")

            # Bulk create OrderItems
            self.order_item_model.objects.bulk_create(order_items_to_create)

            # Update the order's total amount
            order.total_amount = total_amount
            order.save()

            # Clear the cart after successful order creation
            cart.items.all().delete()
            cart.updated_at = timezone.now()
            cart.save()
            
            # Create initial Payment and Shipment records (status: pending)
            # This assumes payment and shipment are separate steps triggered later
            # Payment status will be 'pending' or 'created', Shipment status 'pending'
            payment = self.payment_model.objects.create(
                order=order,
                provider='manual', # Default provider, will be updated after processing
                transaction_id=f'ORDER-{order.pk}-PAYMENT', # Placeholder
                amount=order.total_amount,
                status='pending',
            )
            
            shipment = self.shipment_model.objects.create(
                order=order,
                status='pending',
            )

        # Return the created order object, can be serialized by OrderSerializer
        return order

    def get_user_orders(self, user):
        orders = self.order_model.objects.filter(user=user).select_related('user').prefetch_related('items')
        return self.order_serializer(orders, many=True).data

    def get_order_detail(self, user, order_id):
        try:
            order = self.order_model.objects.get(user=user, pk=order_id)
            serializer = self.order_serializer(order)
            return serializer.data
        except self.order_model.DoesNotExist:
            raise ValueError("Order not found.")

    def update_order_status(self, order, new_status):
        # Basic status update, more complex logic (e.g., payment/shipment status checks) might be needed
        order.status = new_status
        order.save()
        return self.order_serializer(order).data

    def get_order_items(self, order):
        items = order.items.all()
        serializer = self.order_item_serializer(items, many=True)
        return serializer.data

# Example usage:
# from users.models import User
# from addresses.models import Address # Assuming this is how we get address data
# order_service = OrderService()
# user = User.objects.get(pk=1)
# # Assume shipping_address_data and billing_address_data are dicts
# shipping_address_snapshot = {...} 
# billing_address_snapshot = {...}
# order = order_service.create_order_from_cart(user, shipping_address_snapshot, billing_address_snapshot)
# user_orders = order_service.get_user_orders(user)
