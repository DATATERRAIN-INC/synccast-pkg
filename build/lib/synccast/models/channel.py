# synccast/models/channel.py

# Django imports
from django.db import models

# SyncCast abstract model
from synccast.models.base import AbstractSyncCastBaseModel

# syncCast model mixins
from synccast.models.mixins import EnforcedFKTargetsMixin

class AbstractSyncCastChannel(EnforcedFKTargetsMixin, AbstractSyncCastBaseModel):
    """
    Represents an event stream within a scope, e.g., 'message', 'typing', 'presence'.
    Channels live under a scope.
    """

    REQUIRED_FK_TARGETS = [
        "synccast.models.scope.AbstractSyncCastScope"
    ]

    name = models.CharField(
        max_length=100, 
        help_text="Channel name like 'message', 'typing'"
    )

    description = models.TextField(
        blank=True,
        help_text="What this channel is used for."
    )
     
    class Meta:
        abstract = True
