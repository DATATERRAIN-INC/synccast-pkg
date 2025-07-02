# syncast/models/tracker.py

from django.db import models
from django.conf import settings

from syncast.models.base import SyncCastBaseModel
from syncast.models.message import SyncCastMessage

class SyncCastMessageTracker(SyncCastBaseModel):
    """
    Tracks delivery and read status for each user per message.
    """
    message = models.ForeignKey(
        SyncCastMessage,
        on_delete=models.CASCADE,
        related_name="status_receipts",
        help_text="The message this status refers to."
    )
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