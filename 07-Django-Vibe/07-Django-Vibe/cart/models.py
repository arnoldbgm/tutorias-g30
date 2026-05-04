from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator

# from core.models import BaseModel
# from model_utils.models import TimeStampedModel, SoftDeletableModel
# from users.models import User
# from catalog.models import ProductVariant

# class CartBase(TimeStampedModel, SoftDeletableModel):
#     # common fields
#     class Meta:
#         abstract = True

class Cart(models.Model):
    # user = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE, null=True, blank=True) # FK a User
    user = models.OneToOneField('users.User', related_name='cart', on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(_('session key'), max_length=40, null=True, blank=True) # For anonymous users
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.get_full_name() or self.user.email}"
        elif self.session_key:
            return f"Anonymous Cart ({self.session_key})"
        return f"Cart #{self.pk}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    # product_variant = models.ForeignKey(ProductVariant, related_name='cart_items', on_delete=models.CASCADE) # FK a ProductVariant
    product_variant = models.ForeignKey('catalog.ProductVariant', related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('quantity'), validators=[MinValueValidator(1)], default=1)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')
        unique_together = ('cart', 'product_variant') # A cart should not have the same product variant twice

    def __str__(self):
        return f"{self.quantity} of {self.product_variant.sku} in cart #{self.cart.pk}"

    def get_total_price(self):
        return self.quantity * self.product_variant.price
