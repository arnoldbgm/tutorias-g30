# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API URLS
    path('api/v1/auth/', include('users.urls')), # Authentication, User Profile
    path('api/v1/addresses/', include('addresses.urls')),
    path('api/v1/catalog/', include('catalog.urls')),
    path('api/v1/cart/', include('cart.urls')),
    path('api/v1/orders/', include('orders.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/shipments/', include('shipments.urls')),
    # Common app might not need top-level API URLs, or could have utility endpoints
    # path('api/v1/common/', include('common.urls')),

    # Swagger/OpenAPI documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Note: Ensure drf_spectacular is imported in settings.py if it's not already.
# It was added to INSTALLED_APPS in base.py, so this should be fine.
