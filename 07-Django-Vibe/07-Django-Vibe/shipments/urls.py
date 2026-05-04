# shipments/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShipmentViewSet

router = DefaultRouter()
router.register(r'shipments', ShipmentViewSet, basename='shipment')

urlpatterns = [
    path('', include(router.urls)),
    # Custom action for updating shipment status
    # /api/v1/shipments/<int:pk>/update_status/
    path('shipments/<int:pk>/update_status/', ShipmentViewSet.as_view({'post': 'update_status'}), name='shipment-update-status'),
]
