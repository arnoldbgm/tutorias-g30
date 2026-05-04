from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Asumiendo que el modelo User está en 'users.models'
# from users.models import User # Esto se hará más tarde, ahora solo es un placeholder
# from core.models import BaseModel # Si se define un BaseModel abstracto

# Si se usa una librería para soft delete como django-model-utils:
# from model_utils.models import TimeStampedModel, SoftDeletableModel

# class AddressBase(TimeStampedModel, SoftDeletableModel):
#     full_name = models.CharField(_('full name'), max_length=100)
#     phone = models.CharField(_('phone number'), max_length=20)
#     address_line_1 = models.CharField(_('address line 1'), max_length=255)
#     address_line_2 = models.CharField(_('address line 2'), max_length=255, blank=True, null=True)
#     city = models.CharField(_('city'), max_length=100)
#     state = models.CharField(_('state/province'), max_length=100)
#     country = models.CharField(_('country'), max_length=100)
#     postal_code = models.CharField(_('postal code'), max_length=20)

#     class Meta:
#         abstract = True

class Address(models.Model): # Usando modelos estándar de Django por ahora
    # user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE) # FK a User
    user = models.ForeignKey('users.User', related_name='addresses', on_delete=models.CASCADE)
    full_name = models.CharField(_('full name'), max_length=100)
    phone = models.CharField(_('phone number'), max_length=20)
    address_line_1 = models.CharField(_('address line 1'), max_length=255)
    address_line_2 = models.CharField(_('address line 2'), max_length=255, blank=True, null=True)
    city = models.CharField(_('city'), max_length=100)
    state = models.CharField(_('state/province'), max_length=100)
    country = models.CharField(_('country'), max_length=100)
    postal_code = models.CharField(_('postal code'), max_length=20)
    is_default = models.BooleanField(_('is default'), default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"
