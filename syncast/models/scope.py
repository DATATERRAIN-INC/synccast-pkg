# syncast/models/scope.py

from django.db import models
from syncast.models.base import SyncCastBaseModel

class SyncCastScope(SyncCastBaseModel):
    """
    Represents a logical domain of communication, e.g., 'chat', 'program', 'calendar'.
    This is a shared context for multiple channels.
    """
    name = models.CharField(
        max_length=100, 
        unique=True, 
        help_text="Unique scope name like 'chat', 'program', etc."
    )
    description = models.TextField(
        blank=True, 
        help_text="Optional description of what this scope represents."
    )

    class Meta:
        ordering = ["name"]
        abstract = True
 

