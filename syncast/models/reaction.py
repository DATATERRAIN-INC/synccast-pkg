# syncast/models/reaction.py

from django.db import models
from django.conf import settings

from syncast.models.base import AbstractSyncCastBaseModel
from syncast.models.message import AbstractSyncCastMessage

class AbstractSyncCastReaction(AbstractSyncCastBaseModel):
    """
    Represents a reaction to a message, e.g., emojis.
    Tied to a specific message.
    """

    message = models.ForeignKey(
        AbstractSyncCastMessage,
        on_delete=models.CASCADE,
        related_name="reactions",
        help_text="The message this reaction belongs to."
    )

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