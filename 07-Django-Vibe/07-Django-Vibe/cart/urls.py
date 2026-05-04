# cart/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
    # Endpoint to get the current user's cart
    path('cart/', CartViewSet.as_view({'get': 'current'}), name='cart-current'),
    # The CartItemViewSet will be nested under the cart in the URL, e.g., /api/v1/cart/items/
    # However, CartItemViewSet is currently defined to be accessed directly,
    # so we might want to nest it properly in the future if needed.
    # For now, CartViewSet handles the 'current' cart, and CartItemViewSet manages its items.
]
