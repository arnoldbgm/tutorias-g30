# core/models.py
# This app is for core configurations, like base models, constants, etc.

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    """
    An abstract base class that provides self-updating
    created_at and updated_at fields.
    """
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        abstract = True
        ordering = ['-created_at']

# Add any other core models or configurations here.
