# cart/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from catalog.models import ProductVariant # Needed to get product variant details
from django.shortcuts import get_object_or_404
from django.db import transaction

class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing items within a cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated] # Requires authentication

    def get_queryset(self):
        """
        Return cart items for the current user's cart.
        """
        user = self.request.user
        cart = user.cart # Assumes user.cart relationship exists from Cart model
        if cart:
            return CartItem.objects.filter(cart=cart)
        return CartItem.objects.none() # Return empty queryset if no cart

    def perform_create(self, serializer):
        """
        Create a new cart item, associating it with the user's cart.
        Handles adding new items or updating quantity if the item already exists.
        """
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user) # Get or create cart for the user

        product_variant_id = serializer.validated_data.get('product_variant').id
        quantity = serializer.validated_data.get('quantity', 1)

        try:
            product_variant = ProductVariant.objects.get(pk=product_variant_id)
        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError({'product_variant': _('Product variant not found.')})

        # Check if item already exists in cart
        cart_item, item_created = CartItem.objects.get_or_create(
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
            serializer.instance = cart_item # Assign the instance for the serializer
            serializer.save()

        # Update cart's updated_at timestamp
        cart.updated_at = timezone.now()
        cart.save()

    def perform_update(self, serializer):
        """
        Update cart item quantity.
        """
        cart_item = serializer.save()
        cart = cart_item.cart
        cart.updated_at = timezone.now()
        cart.save()

    def perform_destroy(self, instance):
        """
        Delete cart item and update cart's updated_at timestamp.
        """
        cart = instance.cart
        instance.delete()
        cart.updated_at = timezone.now()
        cart.save()

class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the user's shopping cart.
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Return the current user's cart.
        """
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Returns the current user's cart.
        """
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    # Potentially add actions like 'clear_cart', 'apply_coupon', etc.
