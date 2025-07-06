# synccast/models/tracker.py

# Djnago imports
from django.db import models
from django.conf import settings

# SyncCast abstract model
from synccast.models.base import AbstractSyncCastBaseModel

# SyncCast model mixins
from synccast.models.mixins import EnforcedFKTargetsMixin

class AbstractSyncCastReadTracker(EnforcedFKTargetsMixin, AbstractSyncCastBaseModel):
    """
    Tracks delivery and read status for each user per message.
    """

    REQUIRED_FK_TARGETS = [
        "synccast.models.message.AbstractSyncCastMessage"
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="message_statuses",
        help_text="The user receiving or reading the message."
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the message was delivered to the user."
    )
    
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the message was read by the user."
    )

    is_read = models.BooleanField(
        default=False,
        help_text="Flag indicating if the message has been read by the user."
    )

    class Meta:
        abstract = True