from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator

# from users.models import User
# from orders.models import Order
# from common.choices import ShipmentStatusChoices
# from core.models import BaseModel
# from model_utils.models import TimeStampedModel, SoftDeletableModel

# class ShipmentBase(TimeStampedModel, SoftDeletableModel):
#     # common fields
#     class Meta:
#         abstract = True

class Shipment(models.Model):
    # order = models.OneToOneField(Order, related_name='shipment', on_delete=models.CASCADE) # FK to Order
    order = models.OneToOneField('orders.Order', related_name='shipment', on_delete=models.CASCADE)
    tracking_number = models.CharField(_('tracking number'), max_length=255, blank=True, null=True)
    carrier = models.CharField(_('carrier'), max_length=100, blank=True, null=True) # e.g., 'fedex', 'ups', 'dhl'
    # status = models.CharField(_('status'), max_length=50, choices=ShipmentStatusChoices.choices, default=ShipmentStatusChoices.PENDING)
    status = models.CharField(_('status'), max_length=50, default='pending') # Simple string for now
    shipped_at = models.DateTimeField(_('shipped at'), null=True, blank=True)
    delivered_at = models.DateTimeField(_('delivered at'), null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('shipment')
        verbose_name_plural = _('shipments')
        ordering = ['-created_at']

    def __str__(self):
        return f"Shipment for Order #{self.order.pk} ({self.get_status_display() if hasattr(self, 'get_status_display') else self.status})"

    def get_status_display(self):
        # Placeholder for actual status display logic if using choices
        return self.status.capitalize()
