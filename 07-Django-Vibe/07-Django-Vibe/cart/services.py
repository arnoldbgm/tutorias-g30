# cart/services.py
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from catalog.models import ProductVariant
from django.db import transaction
from django.utils import timezone

class CartService:
    def __init__(self):
        self.cart_model = Cart
        self.cart_item_model = CartItem
        self.product_variant_model = ProductVariant
        self.cart_serializer = CartSerializer
        self.cart_item_serializer = CartItemSerializer

    def get_user_cart(self, user):
        cart, created = self.cart_model.objects.get_or_create(user=user)
        serializer = self.cart_serializer(cart)
        return serializer.data

    def add_item_to_cart(self, user, product_variant_id, quantity=1):
        try:
            product_variant = self.product_variant_model.objects.get(pk=product_variant_id, is_active=True)
        except self.product_variant_model.DoesNotExist:
            raise ValueError("Product variant not found or is inactive.")

        cart, created = self.cart_model.objects.get_or_create(user=user)

        # Check if item already exists in cart
        cart_item, item_created = self.cart_item_model.objects.get_or_create(
            cart=cart,
            product_variant=product_variant,
            defaults={'quantity': quantity}
        )

        if not item_created:
            # If item already exists, update quantity
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # If new item, just use the initial quantity
            pass # quantity is already set by defaults or validated_data

        cart.updated_at = timezone.now()
        cart.save()
        
        serializer = self.cart_serializer(cart)
        return serializer.data

    def update_cart_item_quantity(self, user, cart_item_id, quantity):
        try:
            cart_item = self.cart_item_model.objects.get(pk=cart_item_id, cart__user=user)
            if quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
            
            cart = cart_item.cart
            cart.updated_at = timezone.now()
            cart.save()
            serializer = self.cart_serializer(cart)
            return serializer.data
        except self.cart_item_model.DoesNotExist:
            raise ValueError("Cart item not found in your cart.")

    def remove_cart_item(self, user, cart_item_id):
        try:
            cart_item = self.cart_item_model.objects.get(pk=cart_item_id, cart__user=user)
            cart = cart_item.cart
            cart_item.delete()
            cart.updated_at = timezone.now()
            cart.save()
            serializer = self.cart_serializer(cart)
            return serializer.data
        except self.cart_item_model.DoesNotExist:
            raise ValueError("Cart item not found in your cart.")

    def clear_cart(self, user):
        try:
            cart = self.cart_model.objects.get(user=user)
            cart.items.all().delete()
            cart.updated_at = timezone.now()
            cart.save()
            serializer = self.cart_serializer(cart)
            return serializer.data
        except self.cart_model.DoesNotExist:
            # If cart doesn't exist, it's already empty
            return self.cart_serializer(self.cart_model(user=user)).data # Return an empty cart representation

# Example usage:
# from users.models import User
# cart_service = CartService()
# user = User.objects.get(pk=1)
# cart_data = cart_service.get_user_cart(user)
# updated_cart = cart_service.add_item_to_cart(user, product_variant_id=5, quantity=2)
