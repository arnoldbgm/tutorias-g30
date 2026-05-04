# catalog/services.py
from .models import Category, Product, ProductVariant, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ProductVariantSerializer, ProductImageSerializer
from django.db.models import Sum, F
from django.db import transaction

class CatalogService:
    def __init__(self):
        self.category_model = Category
        self.product_model = Product
        self.variant_model = ProductVariant
        self.image_model = ProductImage

        self.category_serializer = CategorySerializer
        self.product_serializer = ProductSerializer
        self.variant_serializer = ProductVariantSerializer
        self.image_serializer = ProductImageSerializer

    def get_categories(self):
        categories = self.category_model.objects.all().order_by('name')
        return self.category_serializer(categories, many=True).data

    def get_products(self, **kwargs):
        # Can accept filters like category, brand, is_active, search terms etc.
        products = self.product_model.objects.filter(**kwargs)
        # Include stock count in the serialized data
        serializer = self.product_serializer(products, many=True, context={'request': kwargs.get('request')})
        return serializer.data

    def get_product_detail(self, product_id):
        try:
            product = self.product_model.objects.get(pk=product_id)
            serializer = self.product_serializer(product)
            return serializer.data
        except self.product_model.DoesNotExist:
            return None

    def get_product_variants(self, product_id):
        try:
            product = self.product_model.objects.get(pk=product_id)
            variants = product.variants.all()
            serializer = self.variant_serializer(variants, many=True)
            return serializer.data
        except self.product_model.DoesNotExist:
            return None

    def get_product_images(self, product_id):
        try:
            product = self.product_model.objects.get(pk=product_id)
            images = product.images.all()
            serializer = self.image_serializer(images, many=True)
            return serializer.data
        except self.product_model.DoesNotExist:
            return None

    def create_product(self, product_data, variants_data=None, images_data=None):
        # Handles creating a product, its variants, and images in a transaction
        with transaction.atomic():
            product_serializer = self.product_serializer(data=product_data)
            product_serializer.is_valid(raise_exception=True)
            product = product_serializer.save()

            if variants_data:
                for variant_data in variants_data:
                    variant_data['product'] = product.id # Link variant to the created product
                    variant_serializer = self.variant_serializer(data=variant_data)
                    variant_serializer.is_valid(raise_exception=True)
                    variant_serializer.save()

            if images_data:
                for image_data in images_data:
                    image_data['product'] = product.id # Link image to the created product
                    image_serializer = self.image_serializer(data=image_data)
                    image_serializer.is_valid(raise_exception=True)
                    image_serializer.save()
            
            return product_serializer.data

    def update_product(self, product, product_data, variants_data=None, images_data=None):
        # This is a simplified update. Full variant/image management might need separate logic or nested routers.
        with transaction.atomic():
            product_serializer = self.product_serializer(product, data=product_data, partial=True)
            product_serializer.is_valid(raise_exception=True)
            product_serializer.save()
            # Variant and image updates would typically be handled via their respective ViewSets/routers
            return product_serializer.data

    def delete_product(self, product):
        product.delete()

    def add_product_variant(self, product_id, variant_data):
        try:
            product = self.product_model.objects.get(pk=product_id)
            variant_data['product'] = product_id
            serializer = self.variant_serializer(data=variant_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except self.product_model.DoesNotExist:
            return None

    def add_product_image(self, product_id, image_data):
        try:
            product = self.product_model.objects.get(pk=product_id)
            image_data['product'] = product_id
            serializer = self.image_serializer(data=image_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except self.product_model.DoesNotExist:
            return None
    
    def get_product_stock(self, product_id):
        # This method might be redundant if get_stock_count is on the model and exposed via serializer.
        # Keeping it here for explicit service layer access if needed.
        try:
            product = self.product_model.objects.get(pk=product_id)
            return product.get_stock_count()
        except self.product_model.DoesNotExist:
            return 0

# Example usage:
# catalog_service = CatalogService()
# products = catalog_service.get_products(is_active=True)
# product_detail = catalog_service.get_product_detail(1)
