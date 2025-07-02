# syncast/models/base.py

from django.db import models
from django.conf import settings

class SyncCastBaseModel(models.Model):

    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if this instance is active."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this instance was created."
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this instance was last updated."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        help_text="User who created this instance."
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        help_text="User who last updated this instance."
    )
     
    class Meta:
        abstract = True
        
