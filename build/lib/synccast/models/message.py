# synccast/models/message.py

# Django imports
from django.db import models
from django.conf import settings

# SyncCast abstract model
from synccast.models.base import AbstractSyncCastBaseModel

# syncCast model mixins
from synccast.models.mixins import EnforcedFKTargetsMixin

class AbstractSyncCastMessage(EnforcedFKTargetsMixin, AbstractSyncCastBaseModel):
    """
    Represents a message in a chat room (group or DM).
    Tied to a Scope via a Room.
    """

    REQUIRED_FK_TARGETS = [
        "synccast.models.room.AbstractSyncCastRoom"
    ]

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        help_text="The user who sent the message."
    )

    content = models.TextField(
        blank=True,
        null=True,
        help_text="The actual message text."
    )

    is_edited = models.BooleanField(
        default=False, 
        help_text="Whether the message was edited."
    )

    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft-delete flag."
    )

    class Meta:
        abstract = True
    
 