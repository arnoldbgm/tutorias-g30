# catalog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductVariantViewSet, ProductImageViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

# Nested routers for product variants and images
# /api/v1/catalog/products/<pk>/variants/
# /api/v1/catalog/products/<pk>/images/
product_router = DefaultRouter()
product_router.register(r'variants', ProductVariantViewSet, basename='product-variant')
product_router.register(r'images', ProductImageViewSet, basename='product-image')

urlpatterns = [
    path('', include(router.urls)),
    # Include nested routers for products
    path('products/<int:product_pk>/', include(product_router.urls)),
]
