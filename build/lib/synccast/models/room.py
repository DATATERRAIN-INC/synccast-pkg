# synccast/models/room.py

# Django imports
from django.db import models
from django.conf import settings

# SyncCast abstract model
from synccast.models.base import AbstractSyncCastBaseModel

# SyncCast model mixins
from synccast.models.mixins import EnforcedFKTargetsMixin

class AbstractSyncCastRoom(EnforcedFKTargetsMixin, AbstractSyncCastBaseModel):
    """
    Represents a communication room which maps to a unique scope instance.
    Used for group chats or direct messages.
    """
    class RoomType(models.TextChoices):
        GROUP = "group", "Group Chat"
        DM = "dm", "Direct Message"

    REQUIRED_FK_TARGETS = [
        "synccast.models.scope.AbstractSyncCastScope"
    ]

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="rooms",
        help_text="Users who are members of this room."
    )

    name = models.CharField(
        max_length=255,
        help_text="Name of the room. Optional for DMs."
    )

    room_image = models.ImageField(
        upload_to='room_images/', 
        null=True, 
        blank=True,
        help_text="Optional image for the room, used in group chats."
    )

    room_type = models.CharField(
        max_length=10,
        choices=RoomType.choices,
        help_text="Type of room: group chat or direct message."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
         
