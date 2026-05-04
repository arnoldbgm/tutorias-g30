# catalog/views.py
from rest_framework import viewsets, permissions, filters
from .models import Category, Product, ProductVariant, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ProductVariantSerializer, ProductImageSerializer
from django_filters.rest_framework import DjangoFilterBackend # Importar DjangoFilterBackend

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing categories.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny] # Publicly accessible

class ProductImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product images.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAdminUser] # Admin only for managing images

    def get_queryset(self):
        """
        Filter images by product if a product ID is provided in the URL.
        """
        queryset = ProductImage.objects.all()
        product_id = self.kwargs.get('product_pk') # Assuming URL pattern includes product_pk
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

    def perform_create(self, serializer):
        """
        Associate image with a product. Assumes product ID is in the URL or request data.
        """
        product_id = self.kwargs.get('product_pk')
        if product_id:
            from .models import Product
            try:
                product = Product.objects.get(pk=product_id)
                serializer.save(product=product)
            except Product.DoesNotExist:
                raise serializers.ValidationError("Product not found.")
        else:
             # Fallback if product_pk is not in URL, try to get from data
             product_id_from_data = self.request.data.get('product')
             if product_id_from_data:
                 from .models import Product
                 try:
                     product = Product.objects.get(pk=product_id_from_data)
                     serializer.save(product=product)
                 except Product.DoesNotExist:
                     raise serializers.ValidationError("Product not found.")
             else:
                 raise serializers.ValidationError("Product ID is required.")


class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product variants.
    """
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAdminUser] # Admin only for managing variants
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['sku', 'is_active', 'product']
    search_fields = ['sku', 'name']
    ordering_fields = ['price', 'stock', 'created_at']

    def get_queryset(self):
        """
        Filter variants by product if a product ID is provided in the URL.
        """
        queryset = ProductVariant.objects.all()
        product_id = self.kwargs.get('product_pk') # Assuming URL pattern includes product_pk
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

    def perform_create(self, serializer):
        """
        Associate variant with a product. Assumes product ID is in the URL or request data.
        """
        product_id = self.kwargs.get('product_pk')
        if product_id:
            from .models import Product
            try:
                product = Product.objects.get(pk=product_id)
                serializer.save(product=product)
            except Product.DoesNotExist:
                raise serializers.ValidationError("Product not found.")
        else:
             # Fallback if product_pk is not in URL, try to get from data
             product_id_from_data = self.request.data.get('product')
             if product_id_from_data:
                 from .models import Product
                 try:
                     product = Product.objects.get(pk=product_id_from_data)
                     serializer.save(product=product)
                 except Product.DoesNotExist:
                     raise serializers.ValidationError("Product not found.")
             else:
                 raise serializers.ValidationError("Product ID is required.")


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser] # Admin only for managing products
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'brand', 'is_active']
    search_fields = ['name', 'description', 'brand']
    ordering_fields = ['name', 'price', 'created_at'] # Note: 'price' requires accessing ProductVariant

    def get_permissions(self):
        """
        Allow anyone to list and retrieve products, but only admins to create, update, delete.
        """
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    # Nested routers for variants and images would be handled in urls.py
    # Example: ProductViewSet with nested variants and images
    # You would typically define these relationships in your urls.py with nested routers.
    # For example, a URL like /api/v1/catalog/products/<pk>/variants/
    # The get_queryset method above is a simplified example assuming product_pk is passed in kwargs.
