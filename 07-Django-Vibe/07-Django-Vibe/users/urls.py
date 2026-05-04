# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='token_create'), # Login endpoint
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Token refresh endpoint
    path('auth/register/', UserViewSet.as_view({'post': 'register'}), name='user_register'), # Registration endpoint
    path('auth/profile/', UserViewSet.as_view({'get': 'profile'}), name='user_profile'), # User profile endpoint
]

