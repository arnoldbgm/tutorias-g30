from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum

# from core.models import BaseModel # Si se define un BaseModel abstracto
# from model_utils.models import TimeStampedModel, SoftDeletableModel

# class CatalogBase(TimeStampedModel, SoftDeletableModel):
#     name = models.CharField(_('name'), max_length=255)
#     slug = models.SlugField(_('slug'), unique=True, max_length=255)
#     # common fields...

#     class Meta:
#         abstract = True

class Category(models.Model): # Usando modelos estándar de Django por ahora
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=255)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.CharField(_('brand'), max_length=100, blank=True, null=True)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_stock_count(self):
        # Calcula el stock total de todas las variantes
        return self.variants.aggregate(total_stock=Sum('stock'))['total_stock'] or 0

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(_('sku'), unique=True, max_length=100)
    name = models.CharField(_('variant name'), max_length=255, blank=True) # e.g., "Large, Red"
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(_('compare price'), max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(_('stock quantity'), default=0)
    weight = models.DecimalField(_('weight'), max_digits=10, decimal_places=3, blank=True, null=True) # e.g., in kg
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('product variant')
        verbose_name_plural = _('product variants')
        ordering = ['sku']

    def __str__(self):
        return f"{self.product.name} - {self.name if self.name else 'Default'} ({self.sku})"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to='products/images/')
    alt_text = models.CharField(_('alt text'), max_length=255, blank=True)
    is_main = models.BooleanField(_('is main'), default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')
        ordering = ['-is_main', 'created_at']

    def __str__(self):
        return f"Image for {self.product.name}"
