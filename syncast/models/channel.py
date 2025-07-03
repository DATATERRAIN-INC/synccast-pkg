# # syncast/models/channel.py

from django.db import models

from syncast.models.scope import AbstractSyncCastScope
from syncast.models.base import AbstractSyncCastBaseModel

class AbstractSyncCastChannel(AbstractSyncCastBaseModel):
    """
    Represents an event stream within a scope, e.g., 'message', 'typing', 'presence'.
    Channels live under a scope.
    """
    name = models.CharField(
        max_length=100, 
        help_text="Channel name like 'message', 'typing'"
    )
    description = models.TextField(
        blank=True,
        help_text="What this channel is used for."
    )
    scope = models.ForeignKey(
        AbstractSyncCastScope, 
        on_delete=models.CASCADE, 
        related_name="channels",
        help_text="The scope this channel belongs to."
    )

    class Meta:
        abstract = True
