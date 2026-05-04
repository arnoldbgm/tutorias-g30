# payments/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    # Custom actions for payment processing and webhooks
    # /api/v1/payments/<int:pk>/process/
    path('payments/<int:pk>/process/', PaymentViewSet.as_view({'post': 'process_payment'}), name='payment-process'),
    # /api/v1/payments/<int:pk>/webhook/
    path('payments/<int:pk>/webhook/', PaymentViewSet.as_view({'post': 'webhook'}), name='payment-webhook'),
]
