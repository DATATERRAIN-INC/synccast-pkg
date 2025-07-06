# synccast/models/reaction.py

# Django imports
from django.db import models
from django.conf import settings

# SyncCast abstract model
from synccast.models.base import AbstractSyncCastBaseModel

# SyncCast model mixins
from synccast.models.mixins import EnforcedFKTargetsMixin

class AbstractSyncCastReaction(EnforcedFKTargetsMixin, AbstractSyncCastBaseModel):
    """
    Represents a reaction to a message, e.g., emojis.
    Tied to a specific message.
    """

    REQUIRED_FK_TARGETS = [
        "synccast.models.message.AbstractSyncCastMessage"
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reactions",
        help_text="The user who reacted."
    )

    emoji = models.CharField(
        max_length=50,
        help_text="The emoji used for the reaction."
    )
    reacted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the reaction was registered by the user."
    )
    class Meta:
        abstract = True