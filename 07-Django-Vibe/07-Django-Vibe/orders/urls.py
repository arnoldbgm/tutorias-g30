# orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

# Nested router for order items under orders
# Example: /api/v1/orders/<int:order_pk>/items/
order_item_router = DefaultRouter()
order_item_router.register(r'items', OrderItemViewSet, basename='order-item')

urlpatterns = [
    path('', include(router.urls)),
    # Include nested router for order items
    path('orders/<int:order_pk>/', include(order_item_router.urls)),
    # Custom action for updating order status (admin only)
    # /api/v1/orders/<int:pk>/update_status/
    path('orders/<int:pk>/update_status/', OrderViewSet.as_view({'post': 'update_status'}), name='order-update-status'),
]
