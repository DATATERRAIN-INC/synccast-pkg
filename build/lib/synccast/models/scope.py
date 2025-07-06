# synccast/models/scope.py

# Django imports
from django.db import models

# SyncCast abstract model
from synccast.models.base import AbstractSyncCastBaseModel

class AbstractSyncCastScope(AbstractSyncCastBaseModel):
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
        abstract = True
 

