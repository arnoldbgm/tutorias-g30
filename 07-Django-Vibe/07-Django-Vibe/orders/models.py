from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator, DecimalValidator
import json

# from users.models import User
# from addresses.models import Address
# from catalog.models import ProductVariant
# from common.choices import OrderStatusChoices # Assuming choices are defined elsewhere
# from core.models import BaseModel
# from model_utils.models import TimeStampedModel, SoftDeletableModel

# class OrderBase(TimeStampedModel, SoftDeletableModel):
#     # common fields
#     class Meta:
#         abstract = True

class Order(models.Model):
    # user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('users.User', related_name='orders', on_delete=models.SET_NULL, null=True)
    # status = models.CharField(_('status'), max_length=50, choices=OrderStatusChoices.choices, default=OrderStatusChoices.PENDING)
    status = models.CharField(_('status'), max_length=50, default='pending') # Simple string for now
    total_amount = models.DecimalField(_('total amount'), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    shipping_address = models.JSONField(_('shipping address'), null=True, blank=True) # Snapshot of address
    billing_address = models.JSONField(_('billing address'), null=True, blank=True) # Snapshot of address
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.pk} - {self.get_status_display() if hasattr(self, 'get_status_display') else self.status}" # Use display method if available

    def get_status_display(self):
        # Placeholder for actual status display logic if using choices
        return self.status.capitalize()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # product_variant = models.ForeignKey(ProductVariant, related_name='order_items', on_delete=models.SET_NULL, null=True)
    product_variant = models.ForeignKey('catalog.ProductVariant', related_name='order_items', on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(_('product name snapshot'), max_length=255)
    sku = models.CharField(_('sku snapshot'), max_length=100)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(_('quantity'), validators=[MinValueValidator(1)])
    total = models.DecimalField(_('total'), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return f"{self.quantity} x {self.product_name} ({self.sku}) in Order #{self.order.pk}"
