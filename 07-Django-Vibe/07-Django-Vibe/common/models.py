# common/models.py
# This app can contain utility models or abstract base models shared across other apps.
# For now, we can leave it empty or add a placeholder.

# Example: A base model for timestamped objects if not using model_utils
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ['-created_at']

# Add any other shared utility models here.
