from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator, DecimalValidator

# from users.models import User
# from orders.models import Order
# from common.choices import PaymentProviderChoices, PaymentStatusChoices
# from core.models import BaseModel
# from model_utils.models import TimeStampedModel, SoftDeletableModel

# class PaymentBase(TimeStampedModel, SoftDeletableModel):
#     # common fields
#     class Meta:
#         abstract = True

class Payment(models.Model):
    # order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE) # FK to Order
    order = models.OneToOneField('orders.Order', related_name='payment', on_delete=models.CASCADE)
    provider = models.CharField(_('payment provider'), max_length=100) # e.g., 'stripe', 'paypal', 'mercadopago'
    transaction_id = models.CharField(_('transaction ID'), max_length=255, unique=True)
    amount = models.DecimalField(_('amount'), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    # status = models.CharField(_('status'), max_length=50, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    status = models.CharField(_('status'), max_length=50, default='pending') # Simple string for now
    paid_at = models.DateTimeField(_('paid at'), null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.transaction_id} for Order #{self.order.pk} ({self.get_status_display() if hasattr(self, 'get_status_display') else self.status})"

    def get_status_display(self):
        # Placeholder for actual status display logic if using choices
        return self.status.capitalize()
